document
  .getElementById("upload-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById("file");
    const file = fileInput.files[0];

    if (!file) {
      alert("Veuillez sélectionner un fichier !");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      const statusDiv = document.getElementById("status");

      if (response.ok) {
        statusDiv.innerHTML = `<p style="color: green;">${
          result.message || "Import réussi !"
        }</p>`;
      } else {
        statusDiv.innerHTML = `<p style="color: red;">Erreur : ${
          result.message || "Échec de l'import."
        }</p>`;
      }
    } catch (error) {
      console.error(error);
      alert("Une erreur s'est produite. Veuillez réessayer.");
    }
  });
