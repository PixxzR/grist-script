export async function loadConfig(projectName) {
  try {
    const response = await fetch(`/configs/${projectName}.json`);

    if (!response.ok) {
      throw new Error(`Configuration "${projectName}" introuvable.`);
    }

    return await response.json();
  } catch (error) {
    console.error(
      `❌ Erreur : Impossible de charger ${projectName}.json`,
      error
    );
    throw error;
  }
}
