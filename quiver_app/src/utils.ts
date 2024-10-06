import type { UTCTimestamp } from "lightweight-charts";

export async function readJsonFile(fileName: string): Promise<any> {
  try {
    const response = await fetch(`${fileName}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    // Convert time to UTC timestamps
    const convertedData = data.map((item: { time: number; value: number }) => ({
      time: (item.time / 1000) as UTCTimestamp, // Convert milliseconds to seconds and cast as UTCTimestamp
      value: item.value,
    }));
    return convertedData;
    // return data;
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
