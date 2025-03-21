const BASE_URL = "https://docs.getgrist.com/api"; // Adapter selon la config
const CORS_PROXY = "http://localhost:8080/"; // Proxy CORS en local

export async function getGristToken() {
  try {
    console.log("🔄 Initialisation du widget Grist...");

    // Vérifier si l'API Grist est disponible
    if (!window.grist) {
      throw new Error("⚠️ L'API Grist n'est pas disponible.");
    }
    grist.ready({ requiredAccess: "full" });
    console.log("✅ Widget prêt, demande d'accès envoyée...");

    // Vérifier si l'API docApi est bien présente
    if (!grist.docApi || !grist.docApi.getAccessToken) {
      throw new Error("⚠️ grist.docApi.getAccessToken() n'est pas disponible.");
    }

    console.log("🔑 Demande d'accès au token en cours...");

    // Récupérer le token
    const tokenInfo = await grist.docApi.getAccessToken({ readOnly: true });

    if (tokenInfo && tokenInfo.token) {
      console.log("🎉 Token Grist reçu :", tokenInfo.token);
      sessionStorage.setItem("gristToken", tokenInfo.token);
      return tokenInfo.token;
    } else {
      throw new Error("⚠️ Token non reçu !");
    }
  } catch (error) {
    console.error(
      "❌ Erreur lors de la récupération du token :",
      error.message
    );
    return null;
  }
}
export async function getGristTokenTest() {
  // 🔹 Utilisation d'un token statique temporairement
  const token =
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZWFkT25seSI6dHJ1ZSwidXNlcklkIjoxMTcyMDYsImRvY0lkIjoiZERyNjlkWXJ3NXprN1U3VFJlYm5ybyIsImlhdCI6MTc0MDA2MTkyMiwiZXhwIjoxNzQwMDYyODIyfQ.05m0m-w8mDVZUs-d6lMhoygKyj_AGM0TMfVEDKSL57Q";
  console.warn("⚠️ Mode développement : utilisation d'un token statique !");
  return token;
}
/**
 * Récupère les enregistrements et colonnes existantes dans Grist.
 * @param {string} docId - ID du document Grist
 * @param {string} tableId - ID de la table
 * @returns {Promise<{records: Object[], columnIds: string[]}>}
 */

export async function getGristData(docId, tableId) {
  try {
    const token = await getGristTokenTest();
    if (!token) throw new Error("Impossible de récupérer le token Grist.");

    // 📌 1️⃣ Récupérer les enregistrements existants via un proxy CORS
    const recordsResponse = await fetch(
      `${CORS_PROXY}${BASE_URL}/docs/${docId}/tables/${tableId}/records`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (!recordsResponse.ok)
      throw new Error("Erreur lors de la récupération des enregistrements.");

    const recordsData = await recordsResponse.json();
    const existingRecords = recordsData.records.map((record) => ({
      id: record.id,
      ...record.fields,
    }));

    // 📌 2️⃣ Récupérer la liste des colonnes via un proxy CORS
    const columnsResponse = await fetch(
      `${CORS_PROXY}${BASE_URL}/docs/${docId}/tables/${tableId}/columns`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (!columnsResponse.ok)
      throw new Error("Erreur lors de la récupération des colonnes.");

    const columnsData = await columnsResponse.json();
    const columnIds = columnsData.columns.map((col) => col.id);

    console.log("📌 Données existantes récupérées :", existingRecords);
    console.log("📌 Colonnes disponibles :", columnIds);

    return { records: existingRecords, columnIds };
  } catch (error) {
    console.error("❌ Erreur dans getGristData :", error.message);
    return { records: [], columnIds: [] };
  }
}
