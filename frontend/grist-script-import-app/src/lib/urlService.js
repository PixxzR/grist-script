// src/lib/urlService.js
export function getProjectNameFromURL() {
  const params = new URLSearchParams(window.location.search);
  const projectName = params.get("project");

  if (!projectName) {
    console.warn(
      "⚠️ Aucun projet spécifié dans l'URL. Utilisation de 'default'."
    );
    return "default"; // Mets un fallback si besoin
  }

  return projectName;
}
