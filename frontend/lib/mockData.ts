export const groups = [
  { id: "203", count: 6, sim: "94–98%", ai: { type: "keep", text: "KEEP 94%" } },
  { id: "204", count: 4, sim: "83–89%", ai: { type: "unsure", text: "UNSURE 85%" } },
  { id: "205", count: 8, sim: "79–82%", ai: { type: "low", text: "LOW CONFIDENCE" } }
] as const;

export const groupThumbnails = [
  { id: "203-1", thumbnail: "linear-gradient(135deg, #2F80ED 0%, #56CCF2 100%)", alt: "Primary suggestion", isPrimary: true },
  { id: "203-2", thumbnail: "linear-gradient(135deg, #F2994A 0%, #F2C94C 100%)", alt: "Alternate 1" },
  { id: "203-3", thumbnail: "linear-gradient(135deg, #EB5757 0%, #F2994A 100%)", alt: "Alternate 2" },
  { id: "203-4", thumbnail: "linear-gradient(135deg, #9B51E0 0%, #56CCF2 100%)", alt: "Alternate 3" },
  { id: "203-5", thumbnail: "linear-gradient(135deg, #27AE60 0%, #6FCF97 100%)", alt: "Alternate 4" },
  { id: "203-6", thumbnail: "linear-gradient(135deg, #F2C94C 0%, #EB5757 100%)", alt: "Alternate 5" }
];
