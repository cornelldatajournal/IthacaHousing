import axios, { type AxiosResponse } from "axios";
import { type Listing, type HeatmapData } from "@/services/interface"

const baseURL = import.meta.env.VITE_API_URL;

/**
 * Fetches listings from PostgreSQL Database
 * @returns Listing[] with all the listings
 */
export const fetchListings = async (): Promise<Listing[]> => {
    try {
        const response: AxiosResponse<Listing[]> = await axios.get(`${baseURL}/listings/`);
        if (response.status === 200) {
            return response.data; 
        } else {
            throw new Error(`Unexpected status code: ${response.status}`);
        }
    } catch (error) {
        console.error("Error fetching listings:", error);
        return []; 
    }
};


/**
 * Fetches top ten listings from PostgreSQL Database
 * @returns Listing[] with the top ten listings
 */
export const fetchTopTenListings = async (): Promise<Listing[]> => {
    try {
        const response: AxiosResponse<Listing[]> = await axios.get(`${baseURL}/top-ten-listings/`);
        if (response.status === 200) {
            return response.data; 
        } else {
            throw new Error(`Unexpected status code: ${response.status}`);
        }
    } catch (error) {
        console.error("Error fetching listings:", error);
        return []; 
    }
};

/**
 * Fetches bottom ten listings from PostgreSQL Database
 * @returns Listing[] with bottom ten listings
 */
export const fetchBottomTenListings = async (): Promise<Listing[]> => {
    try {
        const response: AxiosResponse<Listing[]> = await axios.get(`${baseURL}/bottom-ten-listings/`);
        if (response.status === 200) {
            return response.data; 
        } else {
            throw new Error(`Unexpected status code: ${response.status}`);
        }
    } catch (error) {
        console.error("Error fetching listings:", error);
        return []; 
    }
};


/**
 * Fetches clusters from PostgreSQL Database
 * @returns Listing[] with all the listings, clustered
 */
export const fetchClusters = async (): Promise<Listing[]> => {
    try {
        const response: AxiosResponse<Listing[]> = await axios.get(`${baseURL}/clusters/`);
        if (response.status === 200) {
            return response.data; 
        } else {
            throw new Error(`Unexpected status code: ${response.status}`);
        }
    } catch (error) {
        console.error("Error fetching listings:", error);
        return []; 
    }
};


/**
 * Fetches heatmap from PostgreSQL Database
 * @returns Heatmap data
 */
export const fetchHeatMap = async (): Promise<Number[][]> => {
    try {
        const response: AxiosResponse<HeatmapData> = await axios.get(`${baseURL}/heatmap/`);
        if (response.status === 200) {
            return response.data.heat_data; 
        } else {
            console.log("hi")
            throw new Error(`Unexpected status code: ${response.status}`);
        }
    } catch (error) {
        console.error("Error fetching listings:", error);
        return []; 
    }
};