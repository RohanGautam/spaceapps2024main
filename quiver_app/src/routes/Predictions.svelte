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
    <div class="collapse collapse-plus bg-base-200">
      <input type="radio" name="my-accordion-3" />
      <div class="collapse-title text-xl font-medium">
        Mars Train [Spectogram]
      </div>
      <div class="collapse-content">
        <div class="flex items-center space-x-4 mb-4">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-red-500 mr-2"></div>
            <span>Ground Truth</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-green-500 mr-2"></div>
            <span>Predicted</span>
          </div>
        </div>
        <div class="stats shadow mb-4">
          <div class="stat">
            <div class="stat-title">Mean Absolute Error</div>
            <div class="stat-value">115</div>
          </div>
        </div>
        <img
          src="/results/mars_spec.png"
          alt="Mars Train Spectogram showing ground truth and predicted results"
        />
      </div>
    </div>
    <div class="collapse collapse-plus bg-base-200">
      <input type="radio" name="my-accordion-3" />
      <div class="collapse-title text-xl font-medium">
        Mars Test [Spectogram]
      </div>
      <div class="collapse-content">
        <div class="flex items-center space-x-4 mb-4">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-green-500 mr-2"></div>
            <span>Predicted</span>
          </div>
        </div>
        <img
          src="/results/mars_spec_test.png"
          alt="Mars Test Spectogram showing predicted results"
        />
      </div>
    </div>
    <div class="collapse collapse-plus bg-base-200">
      <input type="radio" name="my-accordion-3" />
      <div class="collapse-title text-xl font-medium">
        Moon Train [Spectogram]
      </div>
      <div class="collapse-content">
        <div class="flex items-center space-x-4 mb-4">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-red-500 mr-2"></div>
            <span>Ground Truth</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-green-500 mr-2"></div>
            <span>Predicted</span>
          </div>
        </div>
        <div class="stats shadow mb-4">
          <div class="stat">
            <div class="stat-title">Mean Absolute Error</div>
            <div class="stat-value">3419</div>
          </div>
        </div>
        <img
          src="/results/moon_spec.png"
          alt="Moon Train Spectogram showing ground truth and predicted results"
        />
      </div>
    </div>
    <div class="collapse collapse-plus bg-base-200">
      <input type="radio" name="my-accordion-3" />
      <div class="collapse-title text-xl font-medium">
        Moon Test [Spectogram]
      </div>
      <div class="collapse-content">
        <div class="flex items-center space-x-4 mb-4">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-green-500 mr-2"></div>
            <span>Predicted</span>
          </div>
        </div>
        <img
          src="/results/moon_spec_test.png"
          alt="Moon Test Spectogram showing predicted results"
        />
      </div>
    </div>
    <div class="collapse collapse-plus bg-base-200">
      <input type="radio" name="my-accordion-3" />
      <div class="collapse-title text-xl font-medium">Mars Train [STA/LTA]</div>
      <div class="collapse-content">
        <div class="flex items-center space-x-4 mb-4">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-red-500 mr-2"></div>
            <span>Ground Truth</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-green-500 mr-2"></div>
            <span>Predicted</span>
          </div>
        </div>
        <div class="stats shadow mb-4">
          <div class="stat">
            <div class="stat-title">Mean Absolute Error</div>
            <div class="stat-value">84.1</div>
          </div>
        </div>
        <img
          src="/results/mars_sta.png"
          alt="Mars Train STA/LTA graph showing ground truth and predicted results"
        />
      </div>
    </div>
    <div class="collapse collapse-plus bg-base-200">
      <input type="radio" name="my-accordion-3" />
      <div class="collapse-title text-xl font-medium">Mars Test [STA/LTA]</div>
      <div class="collapse-content">
        <div class="flex items-center space-x-4 mb-4">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-green-500 mr-2"></div>
            <span>Predicted</span>
          </div>
        </div>
        <img
          src="/results/mars_sta_test.png"
          alt="Mars Test STA/LTA graph showing predicted results"
        />
      </div>
    </div>
    <div class="collapse collapse-plus bg-base-200">
      <input type="radio" name="my-accordion-3" />
      <div class="collapse-title text-xl font-medium">Moon Train [STA/LTA]</div>
      <div class="collapse-content">
        <div class="flex items-center space-x-4 mb-4">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-red-500 mr-2"></div>
            <span>Ground Truth</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-green-500 mr-2"></div>
            <span>Predicted</span>
          </div>
        </div>
        <div class="stats shadow mb-4">
          <div class="stat">
            <div class="stat-title">Mean Absolute Error</div>
            <div class="stat-value">21582</div>
          </div>
        </div>
        <img
          src="/results/moon_sta.png"
          alt="Moon Train STA/LTA graph showing ground truth and predicted results"
        />
      </div>
    </div>
    <div class="collapse collapse-plus bg-base-200">
      <input type="radio" name="my-accordion-3" />
      <div class="collapse-title text-xl font-medium">Moon Test [STA/LTA]</div>
      <div class="collapse-content">
        <div class="flex items-center space-x-4 mb-4">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-green-500 mr-2"></div>
            <span>Predicted</span>
          </div>
        </div>
        <img
          src="/results/moon_sta_test.png"
          alt="Moon Test STA/LTA graph showing predicted results"
        />
      </div>
    </div>
  </main>
</div>
