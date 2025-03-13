document.getElementById("analyzeBtn").addEventListener("click", async () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.scripting.executeScript(
      {
        target: { tabId: tabs[0].id },
        func: getArticleText,
      },
      async (results) => {
        if (results && results[0] && results[0].result) {
          await analyzeArticle(results[0].result);
        } else {
          alert("Could not extract article text.");
        }
      }
    );
  });
});

function getArticleText() {
  let articleElem = document.querySelector("article");
  return articleElem ? articleElem.innerText : document.body.innerText;
}

function analyzeArticle(articleText) {
  fetch("http://127.0.0.1:5000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ article: articleText }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Received Data:", data);
      document.getElementById("biasScore").innerText = `Bias Score: ${data.bias_score}`;
      document.getElementById("biasCategory").innerText = `Bias Level: ${data.bias_category}`;
      document.getElementById("explanation").innerText = `Explanation: ${data.explanation}`;
      document.getElementById("summary").innerText = `Summary: ${data.summary}`;
      document.getElementById("results").style.display = "block";
    })
    .catch((error) => {
      console.error("Error analyzing article:", error);
      alert("Error analyzing article. Make sure the backend server is running.");
    });
}

