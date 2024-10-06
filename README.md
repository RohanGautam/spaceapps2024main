# Quiver: Seismic Data Visualization for Mars and Moon

Quiver is a cutting-edge suite of algorithms paired with an interactive web application, designed as a comprehensive visualization and learning resource for seismic data analysis from Mars and the Moon. It showcases our team's innovative approaches to arrival time prediction and machine learning-based signal analysis, offering researchers, students, and enthusiasts an intuitive platform to explore complex seismic events. Through its interface, users can delve into detailed waveform analyses, high-resolution spectrograms, and comparative views of different prediction methods, while gaining insights into the inner workings of algorithms like STA/LTA, spectral analysis and our custom AI models. By seamlessly integrating advanced analytical techniques with user-friendly visualizations, Quiver serves as a powerful educational tool and research aid, bridging the gap between raw planetary seismic data and meaningful scientific insights, with an emphasis on energy and communication effficiency.

## Features

- Toggle between Mars and Moon data
- Interactive seismic waveform visualization with zoom and pan capabilities
- STA/LTA and spectrogram-based arrival time predictions
- High and low frequency signal visualizations
- Spectrogram display
- High frequency sections visualization

## Installation

To set up Quiver on your local machine, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/your-username/quiver.git
   cd quiver
   ```

2. Set up server:

   ```
   # Create and activate conda environment
   conda create -n quiver_env python=3.9
   conda activate quiver_env

   # Install requirements
   pip install -r requirements.txt

   # Run the server
   cd server
   python server.py # runs uvcorn at http://0.0.0.0:8000 (see console output)
   ```

3. In a seperate terminal, launch frontend:

   ```
   cd quiver_app
   yarn # install deps
   yarn dev # frontend @ http://localhost:5173/ (see console output)
   ```

4. Open your browser and navigate to `http://localhost:5173/` (or the port specified in the console output).

## Usage

1. Use the planet toggle switch to select between Mars and Moon data.
2. Choose a specific data file from the dropdown menu.
3. Explore the seismic waveform using the interactive chart at the top.
4. Examine the processing happening on the lander, orbiter, and Earth station in the cards below.
5. Use the "Get all predictions" button to view predictions for all available data files.

## Contributing

Contributions to Quiver are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
