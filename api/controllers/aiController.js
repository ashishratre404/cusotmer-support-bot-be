const { health, ingest, query, peek } = require("../services/aiService");

exports.aiHealth = async (req, res) => {
  try {
    const data = await health();
    res.json(data);
  } catch (err) {
    console.error("AI Health error:", err.message);
    res.status(500).json({ error: "AI health failed" });
  }
};

exports.ingestDocs = async (req, res) => {
  try {
    const data = await ingest(req.body);
    res.json(data);
  } catch (err) {
    console.error("Ingest error:", err.message);
    res.status(500).json({ error: "Ingest failed" });
  }
};

exports.queryAI = async (req, res) => {
  try {
    const data = await query(req.body);
    res.json(data);
  } catch (err) {
    console.error("Query error:", err.message);
    res.status(500).json({ error: "Query failed" });
  }
};

exports.debugPeek = async (req, res) => {
  try {
    const data = await peek(req.query);
    res.json(data);
  } catch (err) {
    console.error("Peek error:", err.message);
    res.status(500).json({ error: "Peek failed" });
  }
};
