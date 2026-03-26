const filtersReducer = (state, action) => {
  switch (action.type) {
    case 'FETCH_PRODUCTS_START':
      return {
        ...state,
        loading: true,
        error: null,
      };

    case 'FETCH_PRODUCTS_ERROR':
      return {
        ...state,
        loading: false,
        error: action.payload.error,
      };

    case 'LOAD_ALL_PRODUCTS': {
      const { products, minPrice, maxPrice } = action.payload;

      return {
        ...state,
        products,
        allProducts: products,
        selectedPrice: {
          ...state.selectedPrice,
          price: maxPrice,
          minPrice,
          maxPrice,
        },
        loading: false,
        error: null,
      };
    }

    case 'SET_SORTED_VALUE':
      return {
        ...state,
        sortedValue: action.payload.sortValue,
      };

    case 'CHECK_BRANDS_MENU':
      return {
        ...state,
        updatedBrandsMenu: state.updatedBrandsMenu.map((item) => {
          if (item.id === action.payload.id) {
            return {
              ...item,
              checked: !item.checked,
            };
          }
          return item;
        }),
      };

    case 'CHECK_CATEGORY_MENU':
      return {
        ...state,
        updatedCategoryMenu: state.updatedCategoryMenu.map((item) => {
          if (item.id === action.payload.id) {
            return {
              ...item,
              checked: !item.checked,
            };
          }
          return item;
        }),
      };

    case 'HANDLE_PRICE':
      return {
        ...state,
        selectedPrice: {
          ...state.selectedPrice,
          price: action.payload.value,
        },
      };

    case 'FILTERED_PRODUCTS':
      return {
        ...state,
        allProducts: action.payload.updatedProducts,
      };

    case 'MOB_SORT_VISIBILITY':
      return {
        ...state,
        mobFilterBar: {
          ...state.mobFilterBar,
          isMobSortVisible: action.payload.toggle,
        },
      };

    case 'MOB_FILTER_VISIBILITY':
      return {
        ...state,
        mobFilterBar: {
          ...state.mobFilterBar,
          isMobFilterVisible: action.payload.toggle,
        },
      };

    case 'CLEAR_FILTERS':
      return {
        ...state,
        sortedValue: null,
      };

    /* =========================
       REVIEW
    ========================= */

    case 'FETCH_REVIEWS_START':
      return {
        ...state,
        reviewsLoading: true,
        reviewsError: null,
      };

    case 'FETCH_REVIEWS_ERROR':
      return {
        ...state,
        reviewsLoading: false,
        reviewsError: action.payload.error,
        reviews: [],
        originalReviews: [],
      };

    case 'LOAD_PRODUCT_REVIEWS':
      return {
        ...state,
        reviewsLoading: false,
        reviewsError: null,
        reviews: action.payload.reviews,
        originalReviews: action.payload.reviews,
      };

    case 'SET_REVIEW_SORTED_VALUE':
      return {
        ...state,
        reviewSortValue: action.payload.sortValue,
      };

    case 'FILTERED_REVIEWS':
      return {
        ...state,
        reviews: action.payload.updatedReviews,
      };

    case 'CLEAR_REVIEW_FILTERS':
      return {
        ...state,
        reviewSortValue: 'Highest Rating',
        reviews: [...state.originalReviews],
      };

    default:
      return state;
  }
};

export default filtersReducer;