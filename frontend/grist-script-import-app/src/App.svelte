<script>
	import { Router, Route } from "svelte-routing";
	import Header from "./components/Header.svelte";
	import routes from "./routes";
  </script>
  
  <style>
	.container {
	  max-width: 800px;
	  margin: 0 auto;
	  padding: 20px;
	}
  </style>
  
  <Header />
  <div class="container">
	<Router>
	  {#each routes as { path, component }}
		<Route path={path} component={component} />
	  {/each}
	</Router>
  </div>