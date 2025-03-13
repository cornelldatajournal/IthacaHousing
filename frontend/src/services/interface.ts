/**
 * Interface for Housing Listing
 */
export interface Listing {
    id: number;
    address: string;
    price: number;
    bedrooms: number;
    bathrooms: number;
    latitude: number;
    longitude: number;
    listingphotos: JSON;
    differenceInFairValue: number;
}

export interface HeatmapData {
    heat_data: number[][];
}
