chrome.runtime.onMessage.addListener((message) => {
  if (message.action === "highlightBiased") {
    let words = ["propaganda", "fake news", "biased", "misleading"];
    words.forEach(word => {
      document.body.innerHTML = document.body.innerHTML.replace(
        new RegExp(word, "gi"),
        `<mark style="background-color: yellow;">${word}</mark>`
      );
    });
  }
});
