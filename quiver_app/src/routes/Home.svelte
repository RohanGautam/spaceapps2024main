<script lang="ts">
  import { Link } from "svelte-routing";

  import {
    readJsonFile,
    mars_filenames,
    moon_filenames,
    fetchStaltaData,
    fetchSpectrogramData,
    fetchLanderData,
  } from "../utils";
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
  import zoomPlugin from "chartjs-plugin-zoom";

  ChartJS.register(
    Title,
    Tooltip,
    // Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
    annotationPlugin,
    zoomPlugin
  );

  let filenames = mars_filenames;
  let selectedPlanet = "mars";
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
  let staArrivalTimeOriginal: number | null = null;
  let spectrogramArrivalTime: number | null = null;
  let spectrogramImage: string | null = null;
  let lfSignal: string | null = null;
  let hfSignal: string | null = null;

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
        // labels: v.times.filter((_: any, index: number) => index % 15 === 0),
        datasets: [
          {
            // data: v.values.filter((_: any, index: number) => index % 15 === 0),
            data: v.times
              .map((time: number, index: number) => ({
                x: time,
                y: v.values[index],
              }))
              .filter((_: any, index: number) => index % 5 === 0),
            // @ts-ignore
            pointRadius: 0,
            borderColor: "rgb(0,0,0,0.6)",
          },
        ],
      };
      fetchStaltaData(selectedPlanet, filename).then((v) => {
        console.log("stalta", v["arr_time_pred"]);
        if (v.arr_time_pred) {
          staArrivalTime = v.arr_time_pred;
        } else {
          staArrivalTime = null;
        }
        if (v.arr_time) {
          staArrivalTimeOriginal = v.arr_time;
        } else {
          staArrivalTimeOriginal = null;
        }
      });
      fetchSpectrogramData(selectedPlanet, filename).then((v) => {
        console.log("spectrogram", v);
        spectrogramData = v.spectogram;
        spectrogramArrivalTime = v.arr_time_pred;
        // base64 png image string
        spectrogramImage = v.spectogram;
        console.log("spectrogramArrivalTime", spectrogramArrivalTime);
      });
    });
    fetchLanderData(selectedPlanet, filename).then((v) => {
      console.log("lander", v);
      lfSignal = v.lf_signal;
      hfSignal = v.hf_signal;
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
        <Line
          {data}
          width={1100}
          height={100}
          options={{
            responsive: true,
            maintainAspectRatio: true,
            scales: {
              x: {
                type: "linear",
                position: "bottom",
              },
            },
            plugins: {
              zoom: {
                zoom: {
                  wheel: {
                    enabled: true,
                  },
                  pinch: {
                    enabled: true,
                  },
                  mode: "xy",
                },
                pan: {
                  enabled: true,
                  mode: "xy",
                },
              },
            },
          }}
        />
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 flex-grow">
      <div class="card bg-base-100 flex flex-col">
        <div class="card-body flex-grow overflow-y-auto">
          <h2 class="card-title">Lander</h2>
          {#if hfSignal}
            <p class="text-lg font-bold mt-4">High frequency signal</p>
            <img src={hfSignal} alt="HF Signal" class="w-full h-auto mt-2" />
          {/if}
          {#if lfSignal}
            <p class="text-lg font-bold mt-4">Low frequency signal</p>
            <img src={lfSignal} alt="LF Signal" class="w-full h-auto mt-2" />
          {/if}
        </div>
      </div>
      <div class="card bg-base-100 flex flex-col">
        <div class="card-body flex-grow overflow-y-auto">
          <p class="text-lg font-bold">STA/LTA Arrival Time</p>
          <Line
            {data}
            width={200}
            height={120}
            options={{
              responsive: true,
              maintainAspectRatio: true,
              scales: {
                x: {
                  type: "linear",
                  position: "bottom",
                },
              },
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
                    line2: {
                      type: "line",
                      scaleID: "x",
                      value: staArrivalTimeOriginal ?? 0,
                      borderColor: "green",
                      borderWidth: 2,
                      display: staArrivalTimeOriginal !== null,
                    },
                  },
                },
              },
            }}
          />
          <p class="text-lg font-bold">Spectogram Arrival Time</p>
          <Line
            data={{
              labels: data.labels,
              datasets: [
                {
                  data: data.datasets[0].data,
                  borderColor: "rgb(0,0,0,0.6)",
                  pointRadius: 0,
                },
              ],
            }}
            width={200}
            height={120}
            options={{
              responsive: true,
              maintainAspectRatio: true,
              scales: {
                x: {
                  type: "linear",
                  position: "bottom",
                },
              },
              plugins: {
                annotation: {
                  annotations: {
                    line1: {
                      type: "line",
                      scaleID: "x",
                      value: spectrogramArrivalTime ?? 0,
                      borderColor: "red",
                      borderWidth: 2,
                      display: staArrivalTime !== null,
                    },
                    line2: {
                      type: "line",
                      scaleID: "x",
                      value: staArrivalTimeOriginal ?? 0,
                      borderColor: "green",
                      borderWidth: 2,
                      display: staArrivalTimeOriginal !== null,
                    },
                  },
                },
              },
            }}
          />
          {#if spectrogramImage}
            <p class="text-lg font-bold mt-4">Spectrogram</p>
            <img
              src={spectrogramImage}
              alt="Spectrogram"
              class="w-full h-auto mt-2"
            />
          {/if}
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
