<script>
  import { uploadFile } from "../lib/uploadService.js";

  let file = null;
  let status = "";
  let error = "";
  let isLoading = false;

  async function handleUpload() {
    status = "";
    error = "";
    isLoading = true;

    if (!file) {
      error = "Veuillez sélectionner un fichier.";
      isLoading = false;
      return;
    }

    try {
      const result = await uploadFile(file);
      if (result.success) {
        status = "✅ Import réussi !";
        file = null;
        document.getElementById("fileInput").value = ""; // Réinitialise l'input fichier
      } else {
        error = result.message || "❌ Une erreur est survenue.";
      }
    } catch (err) {
      error = "❌ Impossible de se connecter au serveur.";
      console.error(err);
    } finally {
      isLoading = false;
    }
  }
</script>

<style>
  .uploader {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0;
  }

  input[type="file"] {
    margin: 0 auto;
  }

  button {
    background-color: #007bff;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.2s ease;
  }

  button:hover {
    background-color: #0056b3;
  }

  button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }

  .status {
    color: green;
    font-weight: bold;
  }

  .error {
    color: red;
    font-weight: bold;
  }
</style>

<div class="uploader">
  <input
    id="fileInput"
    type="file"
    accept=".xlsx"
    on:change={(e) => (file = e.target.files[0])}
  />
  <button on:click={handleUpload} disabled={isLoading}>
    {isLoading ? "Chargement..." : "Importer le fichier"}
  </button>

  {#if status}
    <p class="status">{status}</p>
  {/if}

  {#if error}
    <p class="error">{error}</p>
  {/if}
</div>