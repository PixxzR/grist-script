<script>
	import Header from "./components/Header.svelte";
	import Router from "svelte-spa-router";
	import routes from "./routes"; // Import des routes configurées
	import { link } from "svelte-spa-router"; // Import de la directive link
  </script>
  
  <style>
	body {
	  font-family: Arial, sans-serif;
	  background-color: #f9f9f9;
	  margin: 0;
	  padding: 0;
	}
  
	nav {
	  background-color: #007bff;
	  padding: 10px;
	  text-align: center;
	}
  
	nav a {
	  color: white;
	  margin: 0 15px;
	  text-decoration: none;
	  font-size: 1.2rem;
	}
  
	nav a:hover {
	  text-decoration: underline;
	}
  
	.app {
	  max-width: 800px;
	  margin: 2rem auto;
	  padding: 2rem;
	  background: white;
	  border-radius: 10px;
	  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	  text-align: center;
	}
  </style>
  
  <!-- Navigation -->
  <nav>
	<a href="/" use:link>Importation</a>
	<a href="/admin" use:link>Administration</a>
  </nav>    
  <div class="app">
	<!-- Header commun -->
	<Header />
  
	<!-- Contenu des pages géré par le routeur -->
	<Router {routes} />
  </div>