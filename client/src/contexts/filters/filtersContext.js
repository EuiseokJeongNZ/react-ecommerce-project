import { createContext, useEffect, useReducer } from 'react';
import { brandsMenu, categoryMenu } from '../../data/filterBarData';
import filtersReducer from './filtersReducer';

const filtersContext = createContext();

const API_BASE = process.env.REACT_APP_API_BASE;
const PRODUCTS_ENDPOINT = `${API_BASE}/api/products/`;

const DEFAULT_PRODUCT_PATH = '/product-details/';

const initialState = {
  products: [],
  allProducts: [],
  sortedValue: null,
  updatedBrandsMenu: brandsMenu,
  updatedCategoryMenu: categoryMenu,
  selectedPrice: {
    price: 0,
    minPrice: 0,
    maxPrice: 0,
  },
  mobFilterBar: {
    isMobSortVisible: false,
    isMobFilterVisible: false,
  },
  loading: false,
  error: null,
};

const FiltersProvider = ({ children }) => {
  const [state, dispatch] = useReducer(filtersReducer, initialState);

  // ✅ 서버 데이터 로딩 (백엔드 응답: { products: [...] })
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        dispatch({ type: 'FETCH_PRODUCTS_START' });

        const res = await fetch(PRODUCTS_ENDPOINT);
        if (!res.ok) throw new Error('Failed to fetch products');

        const data = await res.json();
        const raw = Array.isArray(data.products) ? data.products : [];

        const products = raw.map((p) => {
          const images =
            Array.isArray(p.images) && p.images.length > 0
              ? p.images.map((imgPath) =>
                  String(imgPath).startsWith('http') ? imgPath : `${API_BASE}${imgPath}`
                )
              : ['https://placehold.co/600x600?text=No+Image'];

          return {
            id: p.id,
            title: p.title,
            tag: p.tag,
            tagline: p.tagline,
            brand: p.brand ?? '',
            category: p.category ?? '',
            info: p.info ?? '',
            flavor: p.flavor ?? '',

            finalPrice: Number(p.final_price ?? 0),
            originalPrice: p.original_price != null ? Number(p.original_price) : null,

            rateCount: Math.max(0, Math.round(Number(p.rate_count ?? 0))),

            ratings: Number(p.ratings ?? 0),
            isActive: Boolean(p.is_active),

            images,
            path: DEFAULT_PRODUCT_PATH,
          };
        });

        const priceArr = products.map((item) => item.finalPrice);
        const minPrice = priceArr.length ? Math.min(...priceArr) : 0;
        const maxPrice = priceArr.length ? Math.max(...priceArr) : 0;

        dispatch({
          type: 'LOAD_ALL_PRODUCTS',
          payload: { products, minPrice, maxPrice },
        });
      } catch (e) {
        dispatch({
          type: 'FETCH_PRODUCTS_ERROR',
          payload: { error: e.message || 'Unknown error' },
        });
      }
    };

    fetchProducts();
  }, []);

  const applyFilters = () => {
    let updatedProducts = [...state.products];

    /*==== Sorting ====*/
    if (state.sortedValue) {
      switch (state.sortedValue) {
        case 'Latest':
          updatedProducts = updatedProducts.slice(0, 6).map((item) => item);
          break;

        case 'Featured':
          updatedProducts = updatedProducts.filter((item) => item.tag === 'featured-product');
          break;

        case 'Top Rated':
          updatedProducts = updatedProducts.filter((item) => item.rateCount > 4);
          break;

        case 'Price(Lowest First)':
          updatedProducts = updatedProducts.sort((a, b) => a.finalPrice - b.finalPrice);
          break;

        case 'Price(Highest First)':
          updatedProducts = updatedProducts.sort((a, b) => b.finalPrice - a.finalPrice);
          break;

        default:
          throw new Error('Wrong Option Selected');
      }
    }

    /*==== Filtering ====*/

    // Brands
    const checkedBrandItems = state.updatedBrandsMenu
      .filter((item) => item.checked)
      .map((item) => item.label.toLowerCase());

    if (checkedBrandItems.length) {
      updatedProducts = updatedProducts.filter((item) =>
        checkedBrandItems.includes((item.brand || '').toLowerCase())
      );
    }

    // Category
    const checkedCategoryItems = state.updatedCategoryMenu
      .filter((item) => item.checked)
      .map((item) => item.label.toLowerCase());

    if (checkedCategoryItems.length) {
      updatedProducts = updatedProducts.filter((item) =>
        checkedCategoryItems.includes((item.category || '').toLowerCase())
      );
    }

    // Price
    if (state.selectedPrice) {
      updatedProducts = updatedProducts.filter(
        (item) => item.finalPrice <= Number(state.selectedPrice.price)
      );
    }

    dispatch({
      type: 'FILTERED_PRODUCTS',
      payload: { updatedProducts },
    });
  };

  useEffect(() => {
    if (!state.products.length) return;
    applyFilters();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.products, state.sortedValue, state.updatedBrandsMenu, state.updatedCategoryMenu, state.selectedPrice]);

  // Actions
  const setSortedValue = (sortValue) =>
    dispatch({ type: 'SET_SORTED_VALUE', payload: { sortValue } });

  const handleBrandsMenu = (id) =>
    dispatch({ type: 'CHECK_BRANDS_MENU', payload: { id } });

  const handleCategoryMenu = (id) =>
    dispatch({ type: 'CHECK_CATEGORY_MENU', payload: { id } });

  const handlePrice = (event) => {
    const value = event.target.value;
    return dispatch({ type: 'HANDLE_PRICE', payload: { value } });
  };

  const handleMobSortVisibility = (toggle) =>
    dispatch({ type: 'MOB_SORT_VISIBILITY', payload: { toggle } });

  const handleMobFilterVisibility = (toggle) =>
    dispatch({ type: 'MOB_FILTER_VISIBILITY', payload: { toggle } });

  const handleClearFilters = () => dispatch({ type: 'CLEAR_FILTERS' });

  const values = {
    ...state,
    setSortedValue,
    handleBrandsMenu,
    handleCategoryMenu,
    handlePrice,
    handleMobSortVisibility,
    handleMobFilterVisibility,
    handleClearFilters,
  };

  return <filtersContext.Provider value={values}>{children}</filtersContext.Provider>;
};

export default filtersContext;
export { FiltersProvider };