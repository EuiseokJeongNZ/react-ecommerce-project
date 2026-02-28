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
        products,              // ✅ 원본 저장
        allProducts: products, // ✅ 처음엔 원본 그대로 보여줌
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
        allProducts: action.payload.updatedProducts, // ✅ 화면용만 바꿈
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
        // 필요하면 여기서 brands/category 체크도 초기화 가능
        // updatedBrandsMenu: state.updatedBrandsMenu.map(b => ({...b, checked:false})),
        // updatedCategoryMenu: state.updatedCategoryMenu.map(c => ({...c, checked:false})),
        // selectedPrice: { ...state.selectedPrice, price: state.selectedPrice.maxPrice },
      };

    default:
      return state;
  }
};

export default filtersReducer;