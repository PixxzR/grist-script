<script>
  console.log("AdminPage chargé");

  import { onMount } from "svelte";

  let requiredColumns = [];
  let newColumn = "";
  let message = "";

  let duplicateCheckAttribute = "";
  let selectedMethod = "";
  let docId = "";
  let tableId = "";
  let baseUrl = "";
  let baseUrlOptions = [];
  let customBaseUrl = "";
  let apiKey = "";

  const duplicateMethods = [
      { value: "overwrite", label: "Écraser les valeurs" },
      { value: "replace", label: "Remplacer complètement" },
      { value: "sum", label: "Additionner les valeurs" },
  ];

  async function fetchConfig() {
      try {
          const response = await fetch("http://127.0.0.1:5000/admin/config");
          const result = await response.json();
          requiredColumns = result.required_columns || [];
          duplicateCheckAttribute = result.duplicate_check_attribute || "";
          selectedMethod = result.duplicate_method || "";
          docId = result.doc_id || "";
          tableId = result.table_id || "";
          baseUrl = result.base_url || "";
          baseUrlOptions = result.base_url_options || [];
          apiKey = result.api_key || "";
      } catch (err) {
          console.error("Erreur lors de la récupération de la configuration :", err);
      }
  }

  async function updateConfig() {
      try {
          const updatedBaseUrl = baseUrl === "custom" ? customBaseUrl : baseUrl;

          const response = await fetch("http://127.0.0.1:5000/admin/config", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                  required_columns: requiredColumns,
                  duplicate_check_attribute: duplicateCheckAttribute,
                  duplicate_method: selectedMethod,
                  doc_id: docId,
                  table_id: tableId,
                  base_url: updatedBaseUrl,
                  api_key: apiKey,
              }),
          });
          const result = await response.json();
          message = result.message || "Mise à jour réussie !";
      } catch (err) {
          message = "Erreur lors de la mise à jour.";
          console.error(err);
      }
  }

  function addColumn() {
      if (newColumn && !requiredColumns.includes(newColumn)) {
          requiredColumns = [...requiredColumns, newColumn];
          newColumn = "";
      }
  }

  function removeColumn(column) {
      requiredColumns = requiredColumns.filter((col) => col !== column);
  }

  onMount(fetchConfig);
</script>

<style>
  .admin {
      max-width: 700px;
      margin: 2rem auto;
      font-family: Arial, sans-serif;
  }

  h1 {
      text-align: center;
      color: #333;
      margin-bottom: 1rem;
  }

  .form-group {
      margin-bottom: 1.5rem;
  }

  .form-group label {
      display: block;
      font-weight: bold;
      margin-bottom: 0.5rem;
  }

  .form-group input,
  .form-group select {
      width: 100%;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
      font-size: 1rem;
  }

  ul {
      padding: 0;
      list-style-type: none;
  }

  ul li {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
      padding: 0.5rem 1rem;
      border: 1px solid #ddd;
      border-radius: 5px;
  }

  ul li button {
      background-color: #dc3545;
      color: white;
      border: none;
      border-radius: 5px;
      padding: 5px 10px;
      font-size: 0.9rem;
      cursor: pointer;
  }

  ul li button:hover {
      background-color: #c82333;
  }

  button {
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 5px;
      padding: 10px 20px;
      cursor: pointer;
      font-size: 1rem;
  }

  button:hover {
      background-color: #0056b3;
  }

  .message {
      text-align: center;
      font-weight: bold;
      margin-top: 1rem;
      color: green;
  }

  .section {
      background-color: #f9f9f9;
      border: 1px solid #ddd;
      border-radius: 10px;
      padding: 1.5rem;
      margin-bottom: 2rem;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  .columns-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* Trois colonnes */
        gap: 5px; /* Espacement réduit */
        max-height: 300px; /* Limite de hauteur */
        overflow-y: auto; /* Scroll si nécessaire */
    }

    .column-item {
        background-color: #fff;
        padding: 5px; /* Taille réduite */
        border: 1px solid #ddd;
        border-radius: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.85rem; /* Réduction de la taille du texte */
    }

    .column-item button {
        background-color: #dc3545;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 2px 6px; /* Taille réduite */
        font-size: 0.75rem; /* Texte du bouton plus petit */
        cursor: pointer;
    }

    .column-item button:hover {
        background-color: #c82333;
    }

    input[type="text"] {
        width: 100%;
        padding: 8px; /* Taille réduite */
        margin: 8px 0;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 6px 12px; /* Taille réduite */
        font-size: 0.85rem; /* Réduction de la taille du texte */
    }

    button:hover {
        background-color: #0056b3;
    }

    .message {
        text-align: center;
        font-weight: bold;
        margin-top: 1rem;
        color: green;
    }</style>

<div class="admin">
  <!-- <h1>France Travail Data Manager - Configuration</h1> -->
  <div class="section">
      <h2>Configuration générale</h2>

      <div class="form-group">
          <label for="base-url">Base URL :</label>
          <select id="base-url" bind:value={baseUrl}>
              {#each baseUrlOptions as option}
                  <option value={option}>{option === "custom" ? "Personnalisée" : option}</option>
              {/each}
          </select>
          {#if baseUrl === "custom"}
              <input
                  type="text"
                  placeholder="Entrez une base URL personnalisée"
                  bind:value={customBaseUrl}
              />
          {/if}
      </div>

      <div class="form-group">
          <label for="api-key">Clé API :</label>
          <input
              id="api-key"
              type="text"
              placeholder="Entrez la clé API"
              bind:value={apiKey}
          />
      </div>

      <div class="form-group">
          <label for="doc-id">Document ID :</label>
          <input
              id="doc-id"
              type="text"
              bind:value={docId}
              placeholder="Entrez le Document ID"
          />
      </div>

      <div class="form-group">
          <label for="table-id">Table ID :</label>
          <input
              id="table-id"
              type="text"
              bind:value={tableId}
              placeholder="Entrez le Table ID"
          />
      </div>
  </div>

  <div class="section">
    <h2>Colonnes obligatoires du fichier à importer</h2>
    <div class="columns-grid">
        {#each requiredColumns as column}
            <div class="column-item">
                {column}
                <button on:click={() => removeColumn(column)}>Supprimer</button>
            </div>
        {/each}
    </div>
    <input type="text" bind:value={newColumn} placeholder="Ajouter une colonne" />
    <button on:click={addColumn}>Ajouter</button>
</div>
  <div class="section">
      <h2>Gestion des doublons</h2>
      <div class="form-group">
          <label for="duplicate-attribute">Attribut pour vérifier les doublons :</label>
          <select id="duplicate-attribute" bind:value={duplicateCheckAttribute}>
              <option value="">-- Sélectionner une colonne --</option>
              {#each requiredColumns as column}
                  <option value={column}>{column}</option>
              {/each}
          </select>
      </div>

      <div class="form-group">
          <label>Méthode de gestion :</label>
          {#each duplicateMethods as method}
              <label>
                  <input
                      type="radio"
                      name="duplicate-method"
                      bind:group={selectedMethod}
                      value={method.value}
                  />
                  {method.label}
              </label>
          {/each}
      </div>
  </div>

  <button on:click={updateConfig}>Enregistrer la configuration</button>

  {#if message}
      <p class="message">{message}</p>
  {/if}
</div>