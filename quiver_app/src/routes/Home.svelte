<script lang="ts">
  import { Link } from "svelte-routing";

  let filenames = ["1.mseed", "2.mseed", "3.mseed"];
  let selectedPlanet = "moon";

  function togglePlanet() {
    selectedPlanet = selectedPlanet === "moon" ? "mars" : "moon";
  }
</script>

<div class="flex flex-col min-h-screen">
  <!-- Header -->
  <header class="navbar bg-base-100 shadow-md">
    <div class="flex-1">
      <Link to="/" class="btn btn-ghost normal-case text-xl">Quiver</Link>
    </div>
    <div class="flex-none gap-6">
      <label class="swap swap-rotate">
        <input type="checkbox" on:change={togglePlanet} />
        <div class="swap-off">🌕 Moon</div>
        <div class="swap-on">🔴 Mars</div>
      </label>
      <select class="select select-primary">
        {#each filenames as filename}
          <option value={filename}>{filename}</option>
        {/each}
      </select>
      <button class="btn btn-primary">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6 mr-2"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        Play
      </button>
      <Link to="/predictions" class="btn btn-outline btn-primary"
        >Get all predictions</Link
      >
    </div>
  </header>

  <main class="flex-grow p-4 bg-base-200 flex flex-col">
    <div class="card bg-base-100 w-full mb-4 h-48 overflow-y-auto">
      <div class="card-body p-2">
        <p>
          This card spans the full width of the page, providing ample space for
          important information or a featured section.
        </p>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 flex-grow">
      <div class="card bg-base-100 flex flex-col">
        <div class="card-body flex-grow overflow-y-auto">
          <h2 class="card-title">Lander</h2>
          <p>This is the content for the first card.</p>
        </div>
      </div>
      <div class="card bg-base-100 flex flex-col">
        <div class="card-body flex-grow overflow-y-auto">
          <h2 class="card-title">Orbiter</h2>
          <p>This is the content for the second card.</p>
        </div>
      </div>
      <div class="card bg-base-100 flex flex-col">
        <div class="card-body flex-grow overflow-y-auto">
          <h2 class="card-title">Earth Station</h2>
          <p>This is the content for the third card.</p>
        </div>
      </div>
    </div>
  </main>
</div>
