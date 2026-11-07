/**
 * DevSpire Nexus Registry — JavaScript Static API Example
 * Demonstrates fetching, filtering, and inspecting canonical AI Tools.
 */

const API_BASE_URL = "https://raw.githubusercontent.com/kumaradoss16/DevSpire-Nexus-Registry/main/api/v1";

async function fetchAITools() {
  console.log("Fetching AI Tools from DevSpire Nexus Registry...");
  
  try {
    const response = await fetch(`${API_BASE_URL}/tools.json`);
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    console.log(`Successfully fetched ${data.items.length} tools! (API version: ${data._meta.api_version})\n`);

    // Example 1: Lookup a specific tool
    const chatgpt = data.items.find((item) => item.id === "chatgpt");
    if (chatgpt) {
      console.log(`Tool: ${chatgpt.name} [${chatgpt.category}]`);
      console.log(`URL:  ${chatgpt.official_url}`);
      console.log(`Pricing: ${chatgpt.pricing} (${chatgpt.pricing_class})`);
      console.log(`Status:  ${chatgpt.status}`);
    }

    // Example 2: Filter by category
    const codingTools = data.items.filter((item) => item.category === "Coding & Development");
    console.log(`\nFound ${codingTools.length} Coding & Development tools.`);
    console.log("Top 3:");
    codingTools.slice(0, 3).forEach((tool) => {
      console.log(`  • ${tool.name} - ${tool.official_url}`);
    });

  } catch (error) {
    console.error("Failed to fetch tools:", error);
  }
}

// Execute in Node.js 18+ or modern browsers
if (typeof require !== "undefined" && require.main === module) {
  fetchAITools();
}
