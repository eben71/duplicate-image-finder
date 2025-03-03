import puppeteer, { Browser, Page } from "puppeteer";
import fs from "fs-extra";
import path from "path";
import dotenv from "dotenv";

dotenv.config();

const COOKIES_PATH = path.resolve(__dirname, "../../cookies.json");

export class GooglePhotosScraper {
    private browser: Browser | null = null;
    private page: Page | null = null;

    /** ✅ Start Puppeteer browser */
    async init() {
        this.browser = await puppeteer.launch({
            headless: false, // Set to `true` for production
            args: ["--no-sandbox", "--disable-setuid-sandbox"],
        });

        this.page = await this.browser.newPage();

        // Try to load stored cookies
        await this.loadCookies();
    }

    /** ✅ Load stored cookies (if available) */
    private async loadCookies() {
        if (fs.existsSync(COOKIES_PATH)) {
            const cookies = await fs.readJson(COOKIES_PATH);
            if (this.page) {
                await this.page.setCookie(...cookies);
                console.log("✅ Cookies loaded successfully.");
            }
        } else {
            console.log("⚠️ No saved cookies found. Manual login required.");
        }
    }

    /** ✅ Login to Google Photos */
    async login() {
        if (!this.page) throw new Error("Puppeteer page not initialized.");

        await this.page.goto("https://photos.google.com/", {
            waitUntil: "networkidle2",
        });

        // If already logged in (based on cookies), skip login
        if (this.page.url().includes("photos.google.com")) {
            console.log("✅ Already logged in!");
            return;
        }

        console.log("🔑 Please log in manually in the opened browser...");

        // Wait for the user to complete login
        await this.page.waitForNavigation({ waitUntil: "networkidle2" });

        // Save session cookies after login
        const cookies = await this.page.cookies();
        await fs.writeJson(COOKIES_PATH, cookies);
        console.log("✅ Cookies saved for future sessions.");
    }

    /** ✅ Navigate to albums page */
    async accessAlbums() {
        if (!this.page) throw new Error("Puppeteer page not initialized.");

        await this.page.goto("https://photos.google.com/albums", {
            waitUntil: "networkidle2",
        });

        console.log("📸 Accessed Google Photos albums.");
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
