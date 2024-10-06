<script lang="ts">
  import { Link } from "svelte-routing";

  import {
    readJsonFile,
    mars_filenames,
    moon_filenames,
    fetchStaltaData,
    fetchSpectrogramData,
  } from "../utils";
  import type { IChartApi } from "lightweight-charts";
  import { Line } from "svelte-chartjs";
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
  } from "chart.js";
  import annotationPlugin from "chartjs-plugin-annotation";

  ChartJS.register(
    Title,
    Tooltip,
    // Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
    annotationPlugin
  );

  let filenames = mars_filenames;
  let selectedPlanet = "mars";
  let disp_chart: IChartApi | null;
  let stalta_chart: IChartApi | null;
  let spectrogram_chart: IChartApi | null;
  let selectedFilename = filenames[0];
  let data = {
    labels: [0, 1, 2, 3, 4, 5, 6],
    datasets: [
      {
        data: [0, 1, 2, 3, 4, 5, 6],
      },
    ],
  };
  let spectrogramData = [];
  let staArrivalTime: number | null = null;

  function togglePlanet() {
    selectedPlanet = selectedPlanet === "mars" ? "moon" : "mars";
    filenames = selectedPlanet === "mars" ? mars_filenames : moon_filenames;
    selectedFilename = filenames[0];
    loadData(selectedFilename);
    console.log("togglePlanet", selectedPlanet);
  }

  function loadData(filename: string) {
    readJsonFile(`/data_all/${selectedPlanet}/${filename}`).then((v) => {
      data = {
        labels: v.times.filter((_: any, index: number) => index % 5 === 0),
        datasets: [
          {
            data: v.values.filter((_: any, index: number) => index % 5 === 0),
            // @ts-ignore
            pointRadius: 0,
            borderColor: "rgb(0,0,0,0.6)",
          },
        ],
      };
    });
    fetchStaltaData(selectedPlanet, filename).then((v) => {
      console.log("stalta", v["arr_time_pred"]);
      if (v.arr_time_pred) {
        staArrivalTime = v.arr_time_pred;
      } else {
        staArrivalTime = null;
      }
    });
    fetchSpectrogramData(selectedPlanet, filename).then((v) => {
      console.log("spectrogram", v);
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
        <div class="flex flex-col w-1/3 h-full">
          <!-- stalta -->
          <Line
            {data}
            options={{
              responsive: true,
              maintainAspectRatio: false,
            }}
          />
        </div>
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
          <Line
            {data}
            width={200}
            height={120}
            options={{
              responsive: true,
              maintainAspectRatio: true,
              plugins: {
                annotation: {
                  annotations: {
                    line1: {
                      type: "line",
                      scaleID: "x",
                      value: staArrivalTime ?? 0,
                      borderColor: "red",
                      borderWidth: 2,
                      display: staArrivalTime !== null,
                    },
                  },
                },
              },
            }}
          />
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
