const GOOGLE_API_KEY = "AIzaSyD65Njeo-CvV3yOS3XMsvK2H3KzKmVrI3I";
const LANGUAGE_API_ENDPOINT = "https://language.googleapis.com/v1/documents:analyzeEntities"; // Replace with actual endpoint if different

async function summarizeText(text) {
  const requestBody = {
    document: {
      type: "PLAIN_TEXT",
      content: text
    },
    encodingType: "UTF8"
  };

  try {
    const response = await fetch(`${LANGUAGE_API_ENDPOINT}?key=${GOOGLE_API_KEY}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Extract summary from response if applicable; this might differ based on actual API response
    const summary = data.entities.map(entity => entity.name).join(', '); // Example extraction; adjust based on API response

    return summary || 'No summary available.';
  } catch (error) {
    console.error('Error:', error);
    return 'An error occurred.';
  }
}
