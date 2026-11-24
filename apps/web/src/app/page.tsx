'use client';

import React, { useState, useEffect, useMemo } from 'react';

import { Product, Category, CartItem, Order } from '../types';
import { fetchProducts, fetchCategories } from '../services/api';

import { Navbar } from '../components/Navbar';
import { HeroBanner } from '../components/HeroBanner';
import { ProductCard } from '../components/ProductCard';
import { ProductDetailModal } from '../components/ProductDetailModal';
import { CartDrawer } from '../components/CartDrawer';
import { CheckoutModal } from '../components/CheckoutModal';
import { OrderTrackingModal } from '../components/OrderTrackingModal';
import { SynergyAdvisorModal } from '../components/SynergyAdvisorModal';
import { Footer } from '../components/Footer';

export default function StoreHomePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Filter & Search states
  const [selectedBrand, setSelectedBrand] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [sortBy, setSortBy] = useState<string>('newest');

  // Interactive Cart & Modals
  const [cart, setCart] = useState<CartItem[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isCartOpen, setIsCartOpen] = useState<boolean>(false);
  const [isCheckoutOpen, setIsCheckoutOpen] = useState<boolean>(false);
  const [isTrackingOpen, setIsTrackingOpen] = useState<boolean>(false);
  const [isAdvisorOpen, setIsAdvisorOpen] = useState<boolean>(false);
  const [checkoutVoucher, setCheckoutVoucher] = useState<string>('');

  // Toast notification state
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  // Brands list for quick filtering
  const brandsList = [
    { slug: 'all', name: 'Tất cả hãng' },
    { slug: 'apple', name: 'Apple' },
    { slug: 'nvidia', name: 'NVIDIA' },
    { slug: 'sony', name: 'Sony' },
    { slug: 'samsung', name: 'Samsung' },
    { slug: 'dell', name: 'Dell' },
    { slug: 'asus', name: 'ASUS' },
    { slug: 'lenovo', name: 'Lenovo' },
    { slug: 'google', name: 'Google' },
    { slug: 'bang-olufsen', name: 'Bang & Olufsen' },
    { slug: 'nintendo', name: 'Nintendo' },
    { slug: 'logitech-keychron', name: 'Logitech & Keychron' },
  ];

  // Load initial data from backend API
  const loadData = async () => {
    setLoading(true);
    const [prodRes, catRes] = await Promise.all([
      fetchProducts({
        brand_slug: selectedBrand !== 'all' ? selectedBrand : undefined,
        category_slug: selectedCategory !== 'all' ? selectedCategory : undefined,
        query: searchQuery || undefined,
        sort_by: sortBy,
      }),
      fetchCategories(),
    ]);

    setProducts(prodRes.data);
    setCategories(catRes);
    setLoading(false);
  };

  useEffect(() => {
    loadData();
  }, [selectedBrand, selectedCategory, searchQuery, sortBy]);

  // Cart operations
  const handleAddToCart = (product: Product, quantity = 1) => {
    setCart((prev) => {
      const existing = prev.find((item) => item.product.id === product.id);
      if (existing) {
        return prev.map((item) =>
          item.product.id === product.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        );
      }
      return [...prev, { product, quantity }];
    });
    showToast(`Đã thêm "${product.title}" vào giỏ hàng`);
  };

  const handleUpdateQuantity = (productId: string, quantity: number) => {
    if (quantity <= 0) {
      handleRemoveFromCart(productId);
      return;
    }
    setCart((prev) =>
      prev.map((item) =>
        item.product.id === productId ? { ...item, quantity } : item
      )
    );
  };

  const handleRemoveFromCart = (productId: string) => {
    setCart((prev) => prev.filter((item) => item.product.id !== productId));
  };

  const handleOpenCheckout = (voucher: string) => {
    setCheckoutVoucher(voucher);
    setIsCartOpen(false);
    setIsCheckoutOpen(true);
  };

  const handleOrderSuccess = (order: Order) => {
    setCart([]);
  };

  const totalCartCount = useMemo(() => {
    return cart.reduce((sum, item) => sum + item.quantity, 0);
  }, [cart]);

  return (
    <div className="min-h-screen flex flex-col bg-white text-gray-950 font-sans">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-gray-950 text-white px-4 py-3 rounded-lg shadow-xl font-medium text-xs flex items-center gap-2 border border-gray-800">
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Main Navigation Bar */}
      <Navbar
        cartCount={totalCartCount}
        onOpenCart={() => setIsCartOpen(true)}
        onOpenAdvisor={() => setIsAdvisorOpen(true)}
        onOpenTracking={() => setIsTrackingOpen(true)}
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
        selectedCategory={selectedCategory}
        onSelectCategory={setSelectedCategory}
        selectedBrand={selectedBrand}
        onSelectBrand={setSelectedBrand}
      />

      <main className="max-w-7xl mx-auto px-4 py-8 flex-1 w-full">
        {/* Editorial Hero Showcase Banner */}
        <HeroBanner
          onOpenAdvisor={() => setIsAdvisorOpen(true)}
          onExploreCategory={(cat) => {
            setSelectedCategory(cat);
            setSelectedBrand('all');
          }}
        />

        {/* Brand Filter Bar (Text Only) */}
        <section className="mb-6">
          <div className="flex items-center gap-2 overflow-x-auto no-scrollbar py-2 border-b border-gray-100">
            <span className="text-[11px] font-bold text-gray-400 uppercase tracking-wider whitespace-nowrap mr-2">
              HÃNG SẢN XUẤT:
            </span>
            {brandsList.map((b) => {
              const isSelected = selectedBrand === b.slug;
              return (
                <button
                  key={b.slug}
                  onClick={() => setSelectedBrand(b.slug)}
                  className={`whitespace-nowrap px-3 py-1.5 rounded text-xs transition ${
                    isSelected
                      ? 'bg-gray-950 text-white font-semibold'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {b.name}
                </button>
              );
            })}
          </div>
        </section>

        {/* Product Catalog Controls Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-bold text-gray-950 tracking-tight">
              Danh Mục Sản Phẩm Điện Tử
            </h2>
            <span className="text-xs bg-gray-100 text-gray-700 px-2.5 py-0.5 rounded-full font-semibold">
              {products.length} sản phẩm
            </span>
          </div>

          {/* Sorting Dropdown */}
          <div className="flex items-center gap-2 text-xs">
            <span className="text-gray-500 font-medium">Sắp xếp:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="bg-white border border-gray-300 text-xs font-medium text-gray-900 rounded-lg px-3 py-1.5 focus:outline-none focus:border-gray-950 cursor-pointer"
            >
              <option value="newest">Mới nhất 2026</option>
              <option value="price_asc">Giá: Thấp đến Cao</option>
              <option value="price_desc">Giá: Cao đến Thấp</option>
              <option value="rating">Đánh giá cao nhất</option>
            </select>
          </div>
        </div>

        {/* Loading State or Products Grid */}
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 animate-pulse">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
              <div key={i} className="h-96 rounded-xl bg-gray-100 border border-gray-200 p-4" />
            ))}
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-16 bg-gray-50 rounded-xl border border-gray-200 space-y-3">
            <h3 className="text-base font-bold text-gray-900">Không tìm thấy sản phẩm phù hợp</h3>
            <p className="text-xs text-gray-500 max-w-sm mx-auto">
              Hãy thử chọn lại danh mục hoặc đặt lại từ khóa tìm kiếm để duyệt toàn bộ danh mục sản phẩm.
            </p>
            <button
              onClick={() => {
                setSelectedBrand('all');
                setSelectedCategory('all');
                setSearchQuery('');
              }}
              className="px-4 py-2 bg-gray-950 hover:bg-black text-xs font-semibold text-white rounded-lg transition"
            >
              Xem tất cả sản phẩm
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onSelectProduct={setSelectedProduct}
                onAddToCart={(p) => handleAddToCart(p, 1)}
              />
            ))}
          </div>
        )}

        {/* Customer Reviews Section (Inspired by techstore.jp's CustomerReviewTile) */}
        <section className="mt-20 pt-12 border-t border-gray-200">
          <div className="text-center max-w-2xl mx-auto mb-10 space-y-2">
            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest block">
              PHẢN HỒI TỪ KHÁCH HÀNG DOANH NGHIỆP & CHUYÊN GIA
            </span>
            <h3 className="text-2xl font-bold text-gray-950 tracking-tight">
              Được Tin Dùng Bởi Hơn 15,000 Chuyên Viên Công Nghệ
            </h3>
            <p className="text-xs text-gray-500">
              Đánh giá thực tế từ các kỹ sư AI, đạo diễn điện ảnh và lập trình viên tại Việt Nam và Nhật Bản.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-gray-50 border border-gray-200 space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-gray-950">Nguyễn Quốc Thái</span>
                <span className="text-[10px] font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  Đã mua: MacBook Pro M4 Max
                </span>
              </div>
              <div className="text-xs font-semibold text-gray-900">Đánh giá: 5.0 / 5.0</div>
              <p className="text-xs text-gray-600 leading-relaxed">
                "Máy nguyên seal chính hãng, bàn phím gõ êm, màn hình XDR 120Hz mượt mà tuyệt đối. Thời gian giao hàng chỉ 90 phút tại Quận 1. Rất hài lòng về chất lượng đóng gói."
              </p>
              <div className="text-[11px] text-gray-400">Senior Software Architect • TP. Hồ Chí Minh</div>
            </div>

            <div className="p-6 rounded-xl bg-gray-50 border border-gray-200 space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-gray-950">Trần Đức Anh</span>
                <span className="text-[10px] font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  Đã mua: NVIDIA RTX 5090 FE
                </span>
              </div>
              <div className="text-xs font-semibold text-gray-900">Đánh giá: 5.0 / 5.0</div>
              <p className="text-xs text-gray-600 leading-relaxed">
                "32GB GDDR7 chạy LLaMA-3 70B nội bộ siêu mượt mà không gặp bất kỳ lỗi nào. Đội ngũ kỹ thuật hỗ trợ kiểm tra nhiệt độ và cài đặt driver CUDA rất chuyên nghiệp."
              </p>
              <div className="text-[11px] text-gray-400">Head of AI Lab • Hà Nội</div>
            </div>

            <div className="p-6 rounded-xl bg-gray-50 border border-gray-200 space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-gray-950">Phạm Mai Phương</span>
                <span className="text-[10px] font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  Đã mua: iPhone 16 Pro Max 1TB
                </span>
              </div>
              <div className="text-xs font-semibold text-gray-900">Đánh giá: 5.0 / 5.0</div>
              <p className="text-xs text-gray-600 leading-relaxed">
                "Khung viền Titan Sa Mạc màu ngoài thực tế rất sang trọng và tinh tế. Quay phim 4K 120fps chuẩn Apple Log cho studio dựng phim chất lượng vượt trội so với thế hệ trước."
              </p>
              <div className="text-[11px] text-gray-400">Creative Film Director • Đà Nẵng</div>
            </div>
          </div>
        </section>

        {/* Corporate Consultation Callout Banner */}
        <section className="mt-16 p-8 sm:p-10 rounded-2xl bg-gray-950 text-white flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-gray-800 text-gray-300 uppercase tracking-wider">
              DÀNH CHO DOANH NGHIỆP & DỰ ÁN
            </span>
            <h3 className="text-xl sm:text-2xl font-bold tracking-tight">
              Cần Báo Giá Cấu Hình Dự Án Hoặc Mua Số Lượng Lớn?
            </h3>
            <p className="text-xs text-gray-400 leading-relaxed">
              UteTechStore cung cấp hợp đồng thương mại trọn gói: Hóa đơn điện tử VAT, chính sách chiết khấu theo khối lượng đơn hàng, và hỗ trợ bảo hành tận nơi cho doanh nghiệp trên toàn quốc.
            </p>
          </div>

          <button
            onClick={() => setIsAdvisorOpen(true)}
            className="px-6 py-3 bg-white hover:bg-gray-100 text-gray-950 text-xs font-bold rounded-lg transition flex-shrink-0"
          >
            Liên Hệ Tư Vấn Cấu Hình
          </button>
        </section>
      </main>

      {/* Global Modals & Drawers */}
      <ProductDetailModal
        product={selectedProduct}
        onClose={() => setSelectedProduct(null)}
        onAddToCart={handleAddToCart}
      />

      <CartDrawer
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        items={cart}
        onUpdateQuantity={handleUpdateQuantity}
        onRemoveItem={handleRemoveFromCart}
        onOpenCheckout={handleOpenCheckout}
      />

      <CheckoutModal
        isOpen={isCheckoutOpen}
        onClose={() => setIsCheckoutOpen(false)}
        items={cart}
        voucherCode={checkoutVoucher}
        onOrderSuccess={handleOrderSuccess}
      />

      <OrderTrackingModal
        isOpen={isTrackingOpen}
        onClose={() => setIsTrackingOpen(false)}
      />

      <SynergyAdvisorModal
        isOpen={isAdvisorOpen}
        onClose={() => setIsAdvisorOpen(false)}
        onAddProductToCart={(p) => handleAddToCart(p, 1)}
      />

      {/* Footer */}
      <Footer />
    </div>
  );
}
