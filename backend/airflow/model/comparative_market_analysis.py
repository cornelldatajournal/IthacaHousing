from sklearn.neighbors import NearestNeighbors

def perform_cma(X_with_spatial, apartments_for_rent):
    nbrs = NearestNeighbors(n_neighbors=4, algorithm='ball_tree')  

    nbrs.fit(X_with_spatial)

    distances, indices = nbrs.kneighbors(X_with_spatial)
    listing_ids = apartments_for_rent['ListingId'].values
    nearest_neighbor_listingIds = listing_ids[indices[:, 1:4]]
    apartments_for_rent["nearest_neighbor_listingIds"] = nearest_neighbor_listingIds.tolist()

    return apartments_for_rent