<script lang="ts">
  import { Router, Route } from "svelte-routing";
  import Home from "./routes/Home.svelte";
  import Predictions from "./routes/Predictions.svelte";

  export let url = "";
</script>

<Router {url}>
  <div class="flex flex-col min-h-screen">
    <!-- Router outlet -->
    <Route path="/" component={Home} />
    <Route path="/predictions" component={Predictions} />
  </div>
</Router>

<style>
  /* You can add any global styles here if needed */
</style>
