import * as XLSX from "xlsx";
import { loadConfig } from "./configService.js";

/**
 * Lit et valide un fichier Excel en fonction de la configuration active.
 * @param {File} file - Fichier Excel importé
 * @param {string} configName - Nom du fichier de configuration (ex: "mdph")
 * @returns {Promise<Object[]>} - Retourne un tableau d'objets avec les lignes valides
 */
export async function readAndValidateExcel(file, configName) {
  return new Promise(async (resolve, reject) => {
    try {
      // Charger la configuration du projet
      const config = await loadConfig(configName);
      const requiredColumns = config.required_columns || [];

      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const data = new Uint8Array(event.target.result);
          const workbook = XLSX.read(data, { type: "array" });

          // Prendre la première feuille
          const sheetName = workbook.SheetNames[0];
          const sheet = workbook.Sheets[sheetName];

          // Convertir en JSON
          const jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });

          if (jsonData.length < 2) {
            return reject(new Error("❌ Le fichier est vide ou mal formaté."));
          }

          // **🔹 Récupérer la première ligne non vide comme en-tête 🔹**
          let headers = jsonData.find((row) =>
            row.some(
              (cell) => cell !== undefined && cell !== null && cell !== ""
            )
          );

          if (!headers) {
            return reject(
              new Error("❌ Impossible de détecter les en-têtes du fichier.")
            );
          }

          // **🧹 Nettoyage des noms de colonnes (trim + suppression espaces invisibles)**
          headers = headers.map((col) =>
            col ? col.toString().trim().replace(/\s+/g, " ") : ""
          );

          console.log("📌 Colonnes détectées :", headers);

          // **🔹 Vérifier la présence des colonnes obligatoires 🔹**
          const missingColumns = requiredColumns.filter(
            (col) => !headers.includes(col.trim().replace(/\s+/g, " "))
          );

          if (missingColumns.length > 0) {
            return reject(
              new Error(`❌ Colonnes manquantes : ${missingColumns.join(", ")}`)
            );
          }

          // **📌 Transformer les données en objets**
          const formattedData = jsonData
            .slice(jsonData.indexOf(headers) + 1) // Ignorer les en-têtes
            .map((row) =>
              headers.reduce((acc, header, index) => {
                acc[header] = row[index] || "";
                return acc;
              }, {})
            )
            .filter((row) => Object.values(row).some((value) => value !== "")); // Supprime les lignes vides

          resolve(formattedData);
        } catch (error) {
          reject(new Error("❌ Erreur lors de la lecture du fichier Excel."));
        }
      };

      reader.onerror = () =>
        reject(new Error("❌ Impossible de lire le fichier."));
      reader.readAsArrayBuffer(file);
    } catch (error) {
      reject(
        new Error(
          `❌ Erreur de chargement de la configuration : ${error.message}`
        )
      );
    }
  });
}
