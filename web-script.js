// Detect environment and set API URL accordingly
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_URL = isDevelopment 
    ? "http://127.0.0.1:8000/upload/" 
    : `${window.location.origin}/api/upload/`;

const content = document.getElementById("content");
const form = document.getElementById("form");
const search = document.getElementById("search");
const fileInput = document.getElementById("file-input");
const uploadBox = document.querySelector(".upload-box");
const loading = document.getElementById("loading");
const noResults = document.querySelector(".no-results-placeholder");

let allDocuments = [];

// File upload event listeners
fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
        uploadDocument(file);
    }
});

// Drag and drop functionality
uploadBox.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadBox.classList.add("drag-over");
});

uploadBox.addEventListener("dragleave", () => {
    uploadBox.classList.remove("drag-over");
});

uploadBox.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadBox.classList.remove("drag-over");
    const file = e.dataTransfer.files[0];
    if (file) {
        uploadDocument(file);
    }
});

// Upload and process document
async function uploadDocument(file) {
    if (!file.type.match(/pdf|image/) && !file.name.endsWith('.pdf')) {
        alert("Please upload a PDF or image file");
        return;
    }

    loading.style.display = "flex";
    noResults.style.display = "none";

    try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(API_URL, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Response:", data);

        // Add document to list
        const docData = {
            name: file.name,
            size: (file.size / 1024).toFixed(2),
            timestamp: new Date().toLocaleString(),
            type: data.type || "Unknown",
            entities: data.entities || {},
            text: data.text || "",
        };

        allDocuments.unshift(docData);
        displayDocuments(allDocuments);
        fileInput.value = "";

    } catch (error) {
        console.error("Error:", error);
        alert(`❌ Error: ${error.message}`);
    } finally {
        loading.style.display = "none";
    }
}

// Display documents
function displayDocuments(documents) {
    content.innerHTML = "";

    if (documents.length === 0) {
        noResults.style.display = "block";
        return;
    }

    noResults.style.display = "none";

    documents.forEach((doc, index) => {
        const documentEl = document.createElement("div");
        documentEl.classList.add("document");
        documentEl.innerHTML = `
            <div class="document-header">
                <h3>${doc.name}</h3>
                <span>${doc.type}</span>
            </div>
            <div class="document-info">
                <p><strong>Size:</strong> ${doc.size} KB</p>
                <p><strong>Time:</strong> ${doc.timestamp}</p>
            </div>
            <div class="entities">
                <h4>Entities</h4>
                ${renderEntities(doc.entities)}
            </div>
            <div class="overview">
                <h3>Preview</h3>
                <p>${doc.text.substring(0, 200)}${doc.text.length > 200 ? "..." : ""}</p>
                <button class="view-btn" onclick="viewFullText(${index})">View Full</button>
                <button class="download-btn" onclick="downloadDocument(${index})">Download</button>
            </div>
        `;
        content.appendChild(documentEl);
    });
}

// Render entities
function renderEntities(entities) {
    let html = '<div class="entities-list">';
    let hasEntities = false;

    for (const [key, value] of Object.entries(entities)) {
        if (value && value.length > 0) {
            hasEntities = true;
            const displayValue = Array.isArray(value) ? value.join(", ") : value;
            html += `<span class="entity-tag">${key}: ${displayValue}</span>`;
        }
    }

    if (!hasEntities) {
        html += '<p style="color: rgba(255,255,255,0.5);">No entities detected</p>';
    }

    html += '</div>';
    return html;
}

// View full text
function viewFullText(index) {
    const doc = allDocuments[index];
    const modal = document.createElement("div");
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    `;

    modal.innerHTML = `
        <div style="background: #0a0e27; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 2rem; max-width: 700px; max-height: 80vh; overflow-y: auto;">
            <h3 style="margin-top: 0; color: #fff; margin-bottom: 1rem;">Full Text: ${doc.name}</h3>
            <p style="color: rgba(255,255,255,0.8); line-height: 1.6; white-space: pre-wrap;">${doc.text}</p>
            <button onclick="this.closest('div').parentElement.remove()" style="background: linear-gradient(135deg, #667eea, #f5576c); color: white; border: none; padding: 0.6rem 1.5rem; border-radius: 20px; cursor: pointer; margin-top: 1rem; font-weight: 600;">Close</button>
        </div>
    `;

    document.body.appendChild(modal);
    modal.addEventListener("click", (e) => {
        if (e.target === modal) modal.remove();
    });
}

// Download document
function downloadDocument(index) {
    const doc = allDocuments[index];
    const dataStr = JSON.stringify(doc, null, 2);
    const element = document.createElement("a");
    element.setAttribute(
        "href",
        "data:text/json;charset=utf-8," + encodeURIComponent(dataStr)
    );
    element.setAttribute("download", `${doc.name.split('.')[0]}_extraction.json`);
    element.style.display = "none";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// Search functionality
form.addEventListener("submit", (e) => {
    e.preventDefault();
    const searchTerm = search.value.toLowerCase();

    if (searchTerm) {
        const filtered = allDocuments.filter((doc) => {
            const entityStr = JSON.stringify(doc.entities).toLowerCase();
            const textStr = doc.text.toLowerCase();
            return entityStr.includes(searchTerm) || textStr.includes(searchTerm);
        });

        displayDocuments(filtered);
        search.value = "";
    } else {
        displayDocuments(allDocuments);
    }
});

// Show no results initially
noResults.style.display = "block";
