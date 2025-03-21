<script>
  import { uploadFile } from "../lib/uploadService.js";
  import { readAndValidateExcel } from "../lib/excelReader.js";
  import { getProjectNameFromURL } from "../lib/urlService.js";
  import { getGristData } from "../lib/gristService.js"; // 🔹 Import de Grist

  let file = null;
  let status = "";
  let error = "";
  let isLoading = false;

  // Récupérer le nom du projet depuis l'URL
  let projectName = getProjectNameFromURL();

  // 🔹 Charger les données de Grist au chargement de la page
  async function loadGristData() {
    try {
      console.log(`📌 Chargement des données Grist pour le projet : ${projectName}`);
      
      const { records, columnIds } = await getGristData("u4qF7um48czP", "DATA MDPH"); // Remplace avec tes valeurs
      
      console.log("✅ Données existantes dans Grist :", records);
      console.log("📊 Colonnes disponibles dans Grist :", columnIds);
    } catch (error) {
      console.error("❌ Erreur lors du chargement des données Grist :", error.message);
    }
  }

  // Charger les données Grist au lancement de la page
  loadGristData();

  async function handleFileChange(event) {
    file = event.target.files[0];

    try {
      console.log(`📌 Chargement de la configuration pour : ${projectName}`);

      // 🔹 Passer le projectName à readAndValidateExcel
      const parsedData = await readAndValidateExcel(file, projectName);
      console.log("✅ Données Excel validées :", parsedData);
    } catch (error) {
      console.error(error.message);
    }
  }

  async function handleUpload() {
    status = "";
    error = "";
    isLoading = true;

    if (!file) {
      error = "❌ Veuillez sélectionner un fichier.";
      isLoading = false;
      return;
    }

    try {
      console.log(`📌 Import du fichier pour le projet : ${projectName}`);

      // 🔹 Lire et valider avec la bonne config
      const parsedData = await readAndValidateExcel(file, projectName);
      console.log("📂 Données Excel après validation :", parsedData);

      const result = await uploadFile(file);
      if (result.success) {
        status = "✅ Import réussi !";
        file = null;
        document.getElementById("fileInput").value = ""; // Réinitialise l'input fichier
      } else {
        error = result.message || "❌ Une erreur est survenue.";
      }
    } catch (err) {
      error = `❌ ${err.message}`;
      console.error(err);
    } finally {
      isLoading = false;
    }
  }
</script>
<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    max-width: 500px;
    margin: 3rem auto;
    text-align: center;
  }

  .file-input {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: #f4f4f4;
    border: 1px solid #ddd;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
  }

  input[type="file"] {
    display: none;
  }

  .file-label {
    cursor: pointer;
  }

  .upload-btn {
    background-color: #007bff;
    color: white;
    padding: 12px 20px;
    font-size: 1rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 15px;
  }

  .upload-btn:hover {
    background-color: #0056b3;
  }

  .upload-btn:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }

  .status {
    margin-top: 15px;
    color: green;
    font-weight: bold;
  }

  .error {
    margin-top: 15px;
    color: red;
    font-weight: bold;
  }
</style>

<div class="container">
  <h2>Importer un fichier</h2>
  <p>Sélectionnez le fichier Excel à importer dans Grist.</p>

  <label class="file-input">
    📂 <span class="file-label">{file ? file.name : "Choisir un fichier"}</span>
    <input type="file" accept=".xlsx" on:change={handleFileChange} />
  </label>

  <button class="upload-btn" on:click={handleUpload} disabled={isLoading}>
    {isLoading ? "⏳ Import en cours..." : "📤 Importer le fichier"}
  </button>

  {#if status}
    <p class="status">{status}</p>
  {/if}

  {#if error}
    <p class="error">{error}</p>
  {/if}
</div>