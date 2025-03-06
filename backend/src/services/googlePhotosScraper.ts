import puppeteer, { Browser, Page } from "puppeteer";
import fs from "fs-extra";
import path from "path";
import dotenv from "dotenv";

dotenv.config();

const COOKIES_PATH = path.resolve(__dirname, "../../cookies.json");

export class GooglePhotosScraper {
    private browser: Browser | null = null;
    private page: Page | null = null;

    private credentials: { email: string; password: string } | null = null;

    constructor(credentials?: { email: string; password: string }) {
        if (credentials) {
            this.credentials = credentials;
        }
    }

    /** ✅ Start Puppeteer browser */
    async init() {
        this.browser = await puppeteer.launch({
            headless: false,
            executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", // macOS
            args: [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled" // 🔥 Prevent detection
            ],
        });
        
        this.page = await this.browser.newPage();

        // ✅ Remove Puppeteer detection
        await this.page.evaluateOnNewDocument(() => {
            Object.defineProperty(navigator, "webdriver", { get: () => false });
        });
    
        // Try to load stored cookies
        await this.loadCookies();
    }

    /** ✅ Load stored cookies (if available) */
    private async loadCookies() {
        if (fs.existsSync(COOKIES_PATH)) {
            const cookies = await fs.readJson(COOKIES_PATH);
            if (this.page) {
                await this.browser?.setCookie(...cookies);
                console.log("✅ Cookies loaded successfully.");
            }
        } else {
            console.log("⚠️ No saved cookies found. Manual login required.");
        }
    }

    /** ✅ Login to Google Photos */
    async login() {
        if (!this.page) throw new Error("Puppeteer page not initialized.");
    
        try {
            await this.page.goto("https://photos.google.com/login", {
                waitUntil: "networkidle2",
                timeout: 90000,
            });
    
            console.log("🔑 Please log in manually in the opened browser...");
    
            // ✅ Improved login handling
            await this.handleLoginChallenge();
    
            // ✅ Improved 2FA handling
            const mfaResult = await this.handle2FAChallenge();
            if (!mfaResult.success) {
                throw new Error(`MFA failed: ${mfaResult.message}`);
            }
    
            // ✅ Verify successful login
            await this.verifyLoginSuccess();
    
            // ✅ Save session more securely
            await this.saveSessionCookies();
    
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : "Unknown error occurred";
            console.error("❌ Login process failed:", errorMessage);
            throw new Error("Unable to complete Google Photos login.");
        }
    }

    async handleLoginChallenge() {
        if (!this.page) throw new Error("Puppeteer page is not initialized.");
    
        const loginSelectors = [
            'input[type="email"]', 
            'input[name="identifier"]', 
            'input[aria-label="Email or phone"]'
        ];
    
        for (const selector of loginSelectors) {
            try {
                await this.page.waitForSelector(selector, { timeout: 30000 });
    
                // ✅ Ensure `this.credentials` exists before accessing it
                if (this.credentials && this.credentials.email) {
                    await this.page.type(selector, this.credentials.email);
                    await this.page.keyboard.press('Enter');
                }
                break; // Exit loop once the login field is found
            } catch {
                continue;
            }
        }
    }
    
    async handle2FAChallenge() {
        if (!this.page) throw new Error("Puppeteer page is not initialized.");
    
        const MAX_MFA_WAIT_TIME = 180000; // 3 minutes
        const CHECK_INTERVAL = 5000; // 5 seconds
    
        console.log("🔍 Checking for MFA challenge...");
    
        let startTime = Date.now();
    
        while (Date.now() - startTime < MAX_MFA_WAIT_TIME) {
            try {
                // ✅ Detect any common MFA challenge elements
                const mfaSelector = 'div[data-challenge="2fa"], div[aria-label*="Verify it\'s you"], input[name="totpPin"]';
                await this.page.waitForSelector(mfaSelector, { timeout: CHECK_INTERVAL });
    
                console.warn("⚠️ MFA challenge detected!");
                console.log("📱 Please approve the login on your phone, enter a security code, or use an authenticator app.");
    
                // ✅ Wait for user to complete 2FA
                try {
                    await this.waitForLoginCompletion(MAX_MFA_WAIT_TIME - (Date.now() - startTime));
    
                    console.log("✅ MFA verification successful!");
                    return { success: true, message: "MFA completed successfully." };
                } catch (e) {
                    return { success: false, message: `MFA failed after user interaction. ${e}` };
                }
            } catch (e) {
                // No MFA element found, retry loop
            }
    
            // Wait before checking again
            await new Promise(resolve => setTimeout(resolve, CHECK_INTERVAL));
        }
    
        console.log("✅ No MFA required (or timed out).");
        return { success: true, message: "No MFA detected within the timeout." };
    }
    
    
    async waitForLoginCompletion(timeout: number) {
        if (!this.page) throw new Error("Puppeteer page is not initialized.");
    
        try {
            // ✅ Wait for a known post-login element
            await this.page.waitForSelector('div[aria-label="Search Photos"]', { timeout });
            return; // Login complete
    
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : "Unknown error occurred";
            throw new Error(`Login completion not detected after MFA. Timeout: ${timeout}ms. Error: ${errorMessage}`);
        }
    }
    
    async verifyLoginSuccess() {
        if (!this.page) throw new Error("Puppeteer page is not initialized.");
    
        try {
            await this.page.waitForSelector('div[aria-label="Search Photos"]', { timeout: 45000 });
            console.log("✅ Login Successful");
        } catch {
            throw new Error("Unable to confirm login after MFA.");
        }
    }
    
    async saveSessionCookies() {
        try {
            if (!this.page) throw new Error("Puppeteer page is not initialized.");
    
            const cookies = await this.page.cookies();
            await fs.writeJson(COOKIES_PATH, cookies, {
                spaces: 2,
                encoding: 'utf8'
            });
    
            console.log("🍪 Session cookies securely saved.");
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : "Unknown error occurred";
            console.warn("⚠️ Cookie saving failed:", errorMessage);
        }
    }
    
    /** ✅ Navigate to albums page */
    async accessAlbums() {
        if (!this.page) throw new Error("Puppeteer page not initialized.");

        await this.page.goto("https://photos.google.com/", {
            waitUntil: "networkidle2",
        });

        console.log("📸 Accessed Google Photos.");
    }

    /** ✅ Extract album details */
    async getAlbums() {
        if (!this.page) throw new Error("Puppeteer page not initialized.");

        const albums = await this.page.evaluate(() => {
            return Array.from(document.querySelectorAll("div[data-id]")).map(
                (album) => ({
                    title: album.textContent?.trim() || "Untitled Album",
                    link: album.querySelector("a")?.href || "",
                })
            );
        });

        console.log("📂 Extracted Albums:", albums);
        return albums;
    }

    /** ✅ Close Puppeteer browser */
    async close() {
        if (this.browser) {
            await this.browser.close();
            console.log("🛑 Puppeteer closed.");
        }
    }
}