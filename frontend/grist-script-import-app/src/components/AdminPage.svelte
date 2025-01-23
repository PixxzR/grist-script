<script>
    console.log("AdminPage chargé");
  
    import { onMount } from "svelte";
  
    let requiredColumns = [];
    let newColumn = "";
    let message = "";
  
    let duplicateCheckAttribute = "";
    let selectedMethod = "";
  
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
      } catch (err) {
        console.error("Erreur lors de la récupération de la configuration :", err);
      }
    }
  
    async function updateConfig() {
      try {
        const response = await fetch("http://127.0.0.1:5000/admin/config", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            required_columns: requiredColumns,
            duplicate_check_attribute: duplicateCheckAttribute,
            duplicate_method: selectedMethod,
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
  
    h1, h2 {
      text-align: center;
      color: #333;
    }
  
    .section {
      background-color: #f9f9f9;
      border: 1px solid #ddd;
      border-radius: 10px;
      padding: 1.5rem;
      margin-bottom: 2rem;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
  
    ul {
      padding: 0;
      list-style-type: none;
      margin: 1rem 0;
    }
  
    ul li {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
      background-color: #fff;
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
  
    input[type="text"], select {
      width: 100%;
      padding: 10px;
      margin: 0.5rem 0;
      border: 1px solid #ccc;
      border-radius: 5px;
      font-size: 1rem;
    }
  
    button {
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 5px;
      padding: 10px 20px;
      cursor: pointer;
      font-size: 1rem;
      margin-top: 1rem;
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
  
    .duplicate-config label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: bold;
    }
  
    .duplicate-config input[type="radio"] {
      margin-right: 0.5rem;
    }
  
    .duplicate-config {
      margin-top: 1.5rem;
    }
  </style>
  
  <div class="admin">  
    <div class="section">
      <h2>Configuration des colonnes obligatoires</h2>
      <ul>
        {#each requiredColumns as column}
          <li>
            {column}
            <button on:click={() => removeColumn(column)}>Supprimer</button>
          </li>
        {/each}
      </ul>
      <input type="text" bind:value={newColumn} placeholder="Ajouter une colonne" />
      <button on:click={addColumn}>Ajouter</button>
      <button on:click={updateConfig}>Enregistrer</button>
    </div>
  
    <div class="section duplicate-config">
      <h2>Configuration des doublons</h2>
      <label for="duplicate-attribute">Choisir l'attribut pour vérifier les doublons :</label>
      <select id="duplicate-attribute" bind:value={duplicateCheckAttribute}>
        <option value="">-- Sélectionner une colonne --</option>
        {#each requiredColumns as column}
          <option value={column}>{column}</option>
        {/each}
      </select>
  
      <h3>Méthode de gestion des doublons ( à définir)</h3>
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
        <br />
      {/each}
  
      <button on:click={updateConfig}>Enregistrer la configuration des doublons</button>
    </div>
  
    {#if message}
      <p class="message">{message}</p>
    {/if}
  </div>