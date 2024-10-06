import type { UTCTimestamp } from "lightweight-charts";

export async function readJsonFile(fileName: string): Promise<any> {
  try {
    const response = await fetch(`${fileName}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    // Convert time to relative time starting from zero
    const startTime = data[0].time;
    console.log("startTime", startTime);
    console.log("endTime", data[data.length - 1].time);
    console.log("difference", data[data.length - 1].time - startTime);

    const times = data.map(
      (item: { time: number; value: number }) => item.time - startTime
    );
    const values = data.map(
      (item: { time: number; value: number }) => item.value
    );

    return {
      times: times,
      values: values,
    };
  } catch (error) {
    console.error(`Error reading JSON file ${fileName}:`, error);
    throw error;
  }
}

export const mars_filenames = [
  "XB.ELYSE.02.BHV.2022-01-02HR04_evid0006.json",
  "XB.ELYSE.02.BHV.2022-02-03HR08_evid0005.json",
  "XB.ELYSE.02.BHV.2019-05-23HR02_evid0041.json",
  "XB.ELYSE.02.BHV.2021-10-11HR23_evid0011.json",
  "XB.ELYSE.02.BHV.2019-07-26HR12_evid0033.json",
  "XB.ELYSE.02.BHV.2021-12-24HR22_evid0007.json",
  "XB.ELYSE.02.BHV.2019-07-26HR12_evid0034.json",
  "XB.ELYSE.02.BHV.2022-04-09HR22_evid0002.json",
  "XB.ELYSE.02.BHV.2019-09-21HR03_evid0032.json",
  "XB.ELYSE.02.BHV.2022-05-04HR23_evid0001.json",
  "XB.ELYSE.02.BHV.2021-05-02HR01_evid0017.json",
];

export const moon_filenames = [
  "xa.s12.00.mhz.1970-01-19HR00_evid00002.json",
  "xa.s12.00.mhz.1970-03-26HR00_evid00004.json",
  "xa.s12.00.mhz.1970-03-14HR00_evid00018.json",
  "xa.s12.00.mhz.1971-01-03HR00_evid00057.json",
  "xa.s12.00.mhz.1970-03-25HR00_evid00003.json",
  "xa.s12.00.mhz.1971-06-11HR00_evid00096.json",
];

export const API_BASE_URL = "http://0.0.0.0:8000";

export async function fetchStaltaData(
  planet: string,
  filename: string
): Promise<any> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/stalta/${planet}?q=${filename}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(
      `Error fetching STA/LTA data for ${planet}/${filename}:`,
      error
    );
    throw error;
  }
}

export async function fetchSpectrogramData(
  planet: string,
  filename: string
): Promise<any> {
  console.log("fetchSpectrogramData", planet, filename);
  try {
    const response = await fetch(
      `${API_BASE_URL}/spectogram/${planet}?q=${filename}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(
      `Error fetching spectrogram data for ${planet}/${filename}:`,
      error
    );
    throw error;
  }
}

export async function fetchLanderData(
  planet: string,
  filename: string
): Promise<any> {
  console.log("fetchLanderData", planet, filename);
  try {
    const response = await fetch(
      `${API_BASE_URL}/landerdata/${planet}?q=${filename}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(
      `Error fetching lander data for ${planet}/${filename}:`,
      error
    );
    throw error;
  }
}
