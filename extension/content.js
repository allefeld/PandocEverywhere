console.log("[PE] Pandoc Everywhere")


// ––– attach listeners –––––––––––––––––––––––––––––––––––––––––––––––––––––––

// helper function
const attached = new WeakSet();
function attachKeyListener(doc) {
  if (! doc) return;
  console.log("[PE] Found document");
  if (attached.has(doc)) {
    console.log("[PE] Handler already attached");
  } else {
    attached.add(doc);
    console.log("[PE] Attaching handler");
    doc.addEventListener("keydown", handleKey, true);
  }
}

// main document
attachKeyListener(document);

// static iframes
for (const iframe of document.querySelectorAll('iframe')) {
  if (iframe.contentDocument) {
    attachKeyListener(iframe.contentDocument);
  }
  iframe.addEventListener('load', () => {
    attachKeyListener(iframe.contentDocument);
  });
}

// dynamic iframes
const mo = new MutationObserver((mutations) => {
  for (const m of mutations) {
    for (const node of m.addedNodes) {
      if (node.tagName === 'IFRAME') {
        const iframe = node;
        if (iframe.contentDocument) {
          attachKeyListener(iframe.contentDocument);
        }
        iframe.addEventListener('load', () => {
          attachKeyListener(iframe.contentDocument);
        });
      }
    }
  }
});
mo.observe(document.body, { childList: true, subtree: true });


// ––– handle shortcuts –––––––––––––––––––––––––––––––––––––––––––––––––––––––

function handleKey(e) {
  const editor = e.target.closest('[contenteditable]');
  if (!editor || !editor.isContentEditable) return;

  switch (formatShortcut(e)) {
    case "Pause":
      // html → markdown → html
      editExternal(editor, "markdown");
      break;
    case "Ctrl+Pause":
      // html → html → html
      editExternal(editor, "html+raw_html");
      break;
    case "Alt+Pause":
      // html
      editExternal(editor, "raw");
      break;
  }
}

function formatShortcut(e) {
   if (["Control", "Shift", "Alt", "Meta"].includes(e.key)) return null;
  const keys = [];
  if (e.ctrlKey) keys.push("Ctrl");
  if (e.altKey) keys.push("Alt");
  if (e.shiftKey) keys.push("Shift");
  if (e.metaKey) keys.push("Meta"); // Cmd on Mac
  const mainKey = e.key.length === 1 ? e.key.toUpperCase() : e.key;
  keys.push(mainKey);
  return keys.join("+");
}


// ––– external editor ––––––––––––––––––––––––––––––––––––––––––––––––––––––––

function editExternal(editor, format) {
  console.log("[PE] editExternal");
  editor.contentEditable = "false";
  editor.classList.add("pe-editing");
  return fetch('http://localhost:5000/', {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "text/plain"
    },
    body: JSON.stringify({
      "text": editor.innerHTML,
      "format": format,
      "url": window.location.href
    })
  }).then((response) => {
    if (!response.ok) {
      return response.json().then(err => {
        alert("PandocEverywhere server error.\n" + err.error);
        editor.contentEditable = "true";
        editor.classList.remove("pe-editing");
        return Promise.reject(); // stop further then-chaining
      });
    }
    return response.text();
  }).then((text) => {
    editor.innerHTML = text;
    editor.contentEditable = "true";
    editor.classList.remove("pe-editing");
  }).catch((error) => {  // fetch fails
    alert(
      "Cannot reach PandocEverywhere server.\n" +
      (error.message || error.toString())
    );
    editor.contentEditable = "true";
    editor.classList.remove("pe-editing");
  });
}
