<script lang="ts">
  import { Link } from "svelte-routing";
  import { Chart, LineSeries } from "svelte-lightweight-charts";
  import { readJsonFile, mars_filenames, moon_filenames } from "../utils";
  import type { IChartApi } from "lightweight-charts";

  let filenames = mars_filenames;
  let selectedPlanet = "mars";
  let chartApi: IChartApi | null;
  let selectedFilename = filenames[0];
  let data: any[] = [];

  function togglePlanet() {
    selectedPlanet = selectedPlanet === "mars" ? "moon" : "mars";
    filenames = selectedPlanet === "mars" ? mars_filenames : moon_filenames;
    selectedFilename = filenames[0];
    loadData(selectedFilename);
    console.log("togglePlanet", selectedPlanet);
  }

  function loadData(filename: string) {
    readJsonFile(`/data_all/${selectedPlanet}/${filename}`).then((v) => {
      data = v;
      if (chartApi) {
        console.log("chartApi", chartApi);
        chartApi?.timeScale().fitContent();
      }
    });
  }

  // make this function reactive when the selectedFilename changes
  $: {
    loadData(selectedFilename);
  }

  // Load the first file by default
  loadData(selectedFilename);
</script>

<div class="flex flex-col min-h-screen">
  <!-- Header -->
  <header class="navbar bg-base-100 shadow-md">
    <div class="flex-1">
      <Link to="/" class="btn btn-ghost normal-case text-xl">Quiver</Link>
    </div>
    <div class="flex-none gap-6">
      <label class="swap swap-rotate">
        <input
          type="checkbox"
          on:click={togglePlanet}
          checked={selectedPlanet === "mars"}
        />
        <div class="swap-off">🌕 Moon</div>
        <div class="swap-on">🔴 Mars</div>
      </label>
      <select class="select select-primary" bind:value={selectedFilename}>
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
      <div class="card-body p-4">
        <Chart
          width={500}
          height={150}
          ref={(ref) => (chartApi = ref)}
          timeScale={{
            timeVisible: true,
            minBarSpacing: 0.002,
          }}
        >
          <LineSeries {data} reactive={true} />
        </Chart>
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
