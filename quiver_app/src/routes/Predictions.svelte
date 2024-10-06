<script lang="ts">
  import { Link } from "svelte-routing";
</script>

<div class="flex flex-col min-h-screen">
  <!-- Header -->
  <header class="navbar bg-base-100 shadow-md">
    <div class="flex-1">
      <Link to="/" class="btn btn-ghost normal-case text-xl">Quiver</Link>
    </div>
    <div class="flex-none gap-6">
      <Link to="/predictions" class="btn btn-outline btn-primary"
        >Get all predictions</Link
      >
    </div>
  </header>

  <main class="flex-grow p-4 bg-base-200">
    <h1 class="text-3xl font-bold mb-4">All Predictions</h1>
    <div class="overflow-x-auto">
      <table class="table w-full">
        <thead>
          <tr>
            <th>Date</th>
            <th>Time</th>
            <th>Lander</th>
            <th>Orbiter</th>
            <th>Earth Station</th>
          </tr>
        </thead>
        <tbody>
          <!-- Example rows, replace with actual data -->
          <tr>
            <td>2023-05-01</td>
            <td>12:00:00</td>
            <td>Prediction 1</td>
            <td>Prediction 2</td>
            <td>Prediction 3</td>
          </tr>
          <tr>
            <td>2023-05-01</td>
            <td>13:00:00</td>
            <td>Prediction 4</td>
            <td>Prediction 5</td>
            <td>Prediction 6</td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</div>
