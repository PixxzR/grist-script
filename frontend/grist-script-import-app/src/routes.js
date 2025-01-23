import AdminPage from "./components/AdminPage.svelte";
import FileUploader from "./components/FileUploader.svelte";

export default {
  "/": FileUploader, // Page principale pour l'import
  "/admin": AdminPage, // Page administrateur
};
