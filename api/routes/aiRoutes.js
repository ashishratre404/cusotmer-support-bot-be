const express = require("express");
const router = express.Router();

// Import controllers
const {
  aiHealth,
  ingestDocs,
  queryAI,
  debugPeek,
} = require("../controllers/aiController");

// Define routes
router.get("/health", aiHealth);
router.post("/ingest", ingestDocs);
router.post("/query", queryAI);
router.get("/debug/peek", debugPeek);

module.exports = router;
