// src/lib/gristApi.js
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
