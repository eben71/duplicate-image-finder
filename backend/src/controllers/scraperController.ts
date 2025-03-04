import { Request, Response } from "express";
import { GooglePhotosScraper } from "../services/googlePhotosScraper";

export const scrapeGooglePhotos = async (req: Request, res: Response) => {
    const scraper = new GooglePhotosScraper();

    try {
        await scraper.init();
        await scraper.login();
        await scraper.accessAlbums();
        const albums = await scraper.getAlbums();

        res.json({ success: true, albums });
    } catch (error) {
        console.error("❌ Error scraping Google Photos:", error);
        const errorMessage = error instanceof Error ? error.message : "Unknown error occurred";
        res.status(500).json({ success: false, error: errorMessage });
    } finally {
        await scraper.close();
    }
};
