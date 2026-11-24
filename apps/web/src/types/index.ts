export interface Specification {
  id?: string;
  spec_group: string;
  spec_key: string;
  spec_value: string;
  order_index?: number;
}

export interface Review {
  id: string;
  author_name: string;
  rating: number;
  comment: string;
  verified_purchase: boolean;
  created_at: string;
}

export interface Product {
  id: string;
  title: string;
  slug: string;
  sku: string;
  price: number;
  original_price: number;
  discount_percent: number;
  thumbnail: string;
  brief_desc?: string;
  full_desc?: string;
  stock: number;
  rating: number;
  review_count: number;
  is_featured: boolean;
  is_bundle: boolean;
  badge?: string;
  brand_name?: string;
  category_name?: string;
  key_specs?: Record<string, string>;
  gallery?: string[];
  specifications?: Specification[];
  reviews?: Review[];
  bundle_components?: Product[];
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  icon?: string;
  product_count: number;
}

export interface Brand {
  id: string;
  name: string;
  slug: string;
  logo_url?: string;
  description?: string;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export interface OrderItem {
  id: string;
  product_id?: string;
  product_title: string;
  product_sku: string;
  unit_price: number;
  quantity: number;
  subtotal: number;
}

export interface Order {
  id: string;
  order_code: string;
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  shipping_address: string;
  payment_method: string;
  order_status: string;
  total_amount: number;
  discount_amount: number;
  final_amount: number;
  voucher_code?: string;
  notes?: string;
  created_at: string;
  items: OrderItem[];
}

export interface AdvisorRecommendation {
  title: string;
  subtitle: string;
  matched_iphone?: Product;
  matched_nvidia?: Product;
  synergy_bundle?: Product;
  synergy_reason: string;
  benchmark_scores: Record<string, any>;
  total_savings_vnd: number;
}
