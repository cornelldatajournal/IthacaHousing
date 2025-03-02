import axios, { type AxiosResponse } from "axios";
import { type Listing } from "@/services/interface"

const baseURL = import.meta.env.VITE_API_URL;

/**
 * Fetches listings from PostgreSQL Database
 * @returns Listing[] with all the listings
 */
export const fetchListings = async (): Promise<Listing[]> => {
    try {
        const response: AxiosResponse<Listing[]> = await axios.get(`${baseURL}/listings/`);
        console.log(response)
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

