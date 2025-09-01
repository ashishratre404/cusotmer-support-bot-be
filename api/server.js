const express = require("express");
const cors = require("cors");
require("dotenv").config();

const aiRoutes = require("./routes/aiRoutes");

const app = express();
app.use(cors());
app.use(express.json());

// Health
app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

// AI routes
app.use("/api/ai", aiRoutes);

const PORT = process.env.PORT || 5050;
app.listen(PORT, () =>
  console.log(`Node.js API running on http://localhost:${PORT}`)
);
