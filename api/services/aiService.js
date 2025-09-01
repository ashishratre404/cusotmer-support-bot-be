const axios = require("axios");

const AI_BASE_URL = process.env.AI_BASE_URL || "http://127.0.0.1:8001";

exports.ingest = async (body) => {
  const res = await axios.post(`${AI_BASE_URL}/ingest`, body);
  return res.data;
};

exports.query = async (body) => {
  const res = await axios.post(`${AI_BASE_URL}/query`, body);
  return res.data;
};

exports.peek = async (params) => {
  const res = await axios.get(`${AI_BASE_URL}/debug/peek`, { params });
  return res.data;
};
