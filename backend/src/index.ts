import express from "express";
import { scrapeGooglePhotos } from "./controllers/scraperController";

const app = express();
const PORT = process.env.PORT || 3000;

app.get("/scrape", scrapeGooglePhotos);

app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});
