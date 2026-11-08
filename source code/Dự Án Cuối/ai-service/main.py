"""
AI-Native Commerce AI Service
FastAPI Microservice for NLP Search, Multi-Agent Shopping Assistant & Intent Routing.
Part of FPT Polytechnic NET108 Final Project.
"""

import os
import re
import json
import logging
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import httpx

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ai_service")

app = FastAPI(
    title="AI-Native Commerce AI Service",
    description="Microservice providing NLP Semantic Search, Shopping Agent, and HITL Action Router",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:5000/api/v1")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


# -------------------------------------------------------------
# Request & Response Models
# -------------------------------------------------------------

class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query")
    max_price: Optional[float] = None
    category: Optional[str] = None


class ChatMessage(BaseModel):
    role: str = Field(..., description="'user', 'assistant', or 'system'")
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., description="Current user prompt")
    history: Optional[List[ChatMessage]] = Field(default_factory=list)
    session_id: Optional[str] = "demo-session"
    user_context: Optional[Dict[str, Any]] = None


class ActionApproval(BaseModel):
    action_type: str = Field(..., description="'ADD_TO_CART', 'APPLY_VOUCHER', 'CHECK_ORDER'")
    description: str
    payload: Dict[str, Any]
    requires_confirmation: bool = True


class ChatResponse(BaseModel):
    reply: str
    intent: str
    suggested_products: List[Dict[str, Any]] = []
    suggested_actions: List[str] = []
    proposed_action: Optional[ActionApproval] = None


class RecommendRequest(BaseModel):
    product_id: Optional[str] = None
    cart_items: Optional[List[str]] = []
    limit: Optional[int] = 4


# -------------------------------------------------------------
# Helper Functions & Mock Knowledge Base
# -------------------------------------------------------------

KNOWLEDGE_BASE = [
    {
        "id": "prod-1",
        "name": "Laptop Dell XPS 13 Plus 9320 (Core i7 / 16GB / 512GB SSD)",
        "price": 32990000,
        "category": "Laptop & Máy tính",
        "tags": ["mong-nhe", "van-phong", "do-hoa", "pin-trau", "cao-cap"],
        "description": "Laptop doanh nhân siêu mỏng nhẹ, màn hình 3.5K OLED rực rỡ, pin 12 giờ."
    },
    {
        "id": "prod-2",
        "name": "MacBook Air M3 15-inch (8-Core GPU / 16GB / 512GB)",
        "price": 37990000,
        "category": "Laptop & Máy tính",
        "tags": ["mong-nhe", "pin-trau", "hoc-tap", "van-phong", "apple"],
        "description": "Thời lượng pin tới 18 giờ, không quạt tản nhiệt yên tĩnh tuyệt đối, chip M3 thế hệ mới."
    },
    {
        "id": "prod-3",
        "name": "Tai nghe Sony WH-1000XM5 Chống Ồn Chủ Động",
        "price": 7990000,
        "category": "Phụ kiện & Âm thanh",
        "tags": ["chong-on", "pin-trau", "am-thanh-hifi", "du-lich"],
        "description": "Chống ồn hàng đầu thế giới với 8 micro, đàm thoại AI siêu nét, pin 30 giờ."
    },
    {
        "id": "prod-4",
        "name": "Bàn phím cơ không dây Keychron Q1 Pro QMK/VIA",
        "price": 4290000,
        "category": "Phụ kiện & Âm thanh",
        "tags": ["ban-phim-co", "lap-trinh", "gaming", "custom"],
        "description": "Thân nhôm CNC nguyên khối, gasket mount êm ái, switch switch hot-swap."
    },
    {
        "id": "prod-5",
        "name": "Chuột không dây Logitech MX Master 3S",
        "price": 2490000,
        "category": "Phụ kiện & Âm thanh",
        "tags": ["van-phong", "ergonomic", "pin-trau", "lap-trinh"],
        "description": "Cảm biến 8K DPI mọi bề mặt, nút cuộn từ tính MagSpeed siêu êm ái."
    },
    {
        "id": "prod-6",
        "name": "Cà phê Arabica Cầu Đất Thượng Hạng (Rang Mộc 500g)",
        "price": 280000,
        "category": "Đời sống & Tiện ích",
        "tags": ["cafe", "tinh-tao", "huong-hoa-qua", "thu-cong"],
        "description": "100% Arabica Cầu Đất Đà Lạt, độ cao 1.600m, hương vị thanh tao dịu chua ngọt sâu."
    }
]


def extract_price_constraint(query: str) -> Optional[float]:
    q = query.lower()
    match = re.search(r'dưới\s+(\d+)\s*(triệu|tr|k)', q)
    if match:
        num = float(match.group(1))
        unit = match.group(2)
        if unit in ['triệu', 'tr']:
            return num * 1_000_000
        elif unit == 'k':
            return num * 1_000
    return None


def search_products(query: str, max_price: Optional[float] = None) -> List[Dict[str, Any]]:
    tokens = [t.lower() for t in re.findall(r'\w+', query) if len(t) > 1]
    scored = []
    
    for item in KNOWLEDGE_BASE:
        score = 0
        corpus = f"{item['name']} {item['description']} {' '.join(item['tags'])} {item['category']}".lower()
        
        for t in tokens:
            if t in corpus:
                score += 2
        
        # Semantic boosters
        if "mỏng nhẹ" in query.lower() and "mong-nhe" in item["tags"]:
            score += 4
        if "pin trâu" in query.lower() and "pin-trau" in item["tags"]:
            score += 4
        if "tai nghe" in query.lower() and "tai nghe" in item["name"].lower():
            score += 5
        if "lập trình" in query.lower() and ("lap-trinh" in item["tags"] or "laptop" in item["name"].lower()):
            score += 4
        
        # Price constraint penalty
        if max_price and item["price"] > max_price:
            score -= 10
            
        if score > 0:
            scored.append((score, item))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored]


# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------

@app.get("/")
def read_root():
    return {
        "service": "AI-Native Commerce AI Service",
        "status": "online",
        "version": "1.0.0",
        "capabilities": [
            "NLP Semantic Product Search",
            "Conversational Shopping Assistant (HITL Agent)",
            "Return Policy Reasoner",
            "Contextual Upsell & Cross-sell"
        ]
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ai-service", "timestamp": "OK"}


@app.post("/api/ai/search")
def api_search(req: SearchRequest):
    price_limit = req.max_price or extract_price_constraint(req.query)
    results = search_products(req.query, price_limit)
    
    return {
        "query": req.query,
        "price_filter": price_limit,
        "match_count": len(results),
        "products": results
    }


@app.post("/api/ai/chat", response_model=ChatResponse)
async def api_chat(req: ChatRequest):
    message = req.message.strip().lower()
    
    # 1. Intent: ORDER_TRACKING
    if any(k in message for k in ["đơn hàng", "tra cứu đơn", "mã đơn", "order", "vận chuyển"]):
        return ChatResponse(
            reply="Chào bạn! Tôi có thể hỗ trợ bạn kiểm tra tiến độ đơn hàng. Bạn có thể cung cấp mã đơn hàng (ví dụ: ORD-DEMO-001) hoặc xem trực tiếp trong mục 'Lịch sử đơn hàng' trên tài khoản của bạn.",
            intent="ORDER_TRACKING",
            suggested_actions=[
                "Xem đơn hàng ORD-DEMO-001",
                "Chính sách đổi trả trong 7 ngày",
                "Liên hệ hotline hỗ trợ"
            ]
        )
    
    # 2. Intent: RETURN_POLICY
    if any(k in message for k in ["đổi trả", "hoàn tiền", "bảo hành", "trả hàng", "hư hại"]):
        return ChatResponse(
            reply="Hệ thống AI-Native Commerce áp dụng chính sách đổi trả minh bạch:\n"
                  "1. Thời hạn: Trong vòng 7 ngày kể từ khi đơn hàng ở trạng thái 'DELIVERED'.\n"
                  "2. Điều kiện: Sản phẩm còn nguyên tem mác, hộp và đầy đủ phụ kiện kèm theo.\n"
                  "3. Hỗ trợ tự động: AI Return Agent sẽ phê duyệt tự động cấp mã vận đơn thu hồi nếu đạt điều kiện.",
            intent="RETURN_POLICY",
            suggested_actions=[
                "Yêu cầu hoàn trả đơn gần nhất",
                "Xem chi tiết điều khoản bảo hành"
            ]
        )
    
    # 3. Intent: CART_ACTION (HITL - Propose Add to Cart)
    if any(k in message for k in ["thêm vào giỏ", "mua", "đặt mua", "lấy con", "chọn con"]):
        target_product = None
        for item in KNOWLEDGE_BASE:
            if any(t in message for t in [item["name"].lower()[:12], item["id"].lower()]):
                target_product = item
                break
        
        if not target_product:
            target_product = KNOWLEDGE_BASE[0] # Dell XPS fallback
            
        return ChatResponse(
            reply=f"Tôi đã tìm thấy sản phẩm **{target_product['name']}** với giá ưu đãi **{target_product['price']:,} đ**. Bạn có muốn tôi hỗ trợ thêm sản phẩm này vào giỏ hàng ngay không?",
            intent="CART_ACTION",
            suggested_products=[target_product],
            suggested_actions=[
                "Đồng ý thêm vào giỏ",
                "Xem chi tiết sản phẩm",
                "Tìm sản phẩm khác"
            ],
            proposed_action=ActionApproval(
                action_type="ADD_TO_CART",
                description=f"Thêm {target_product['name']} (SL: 1) vào giỏ hàng cá nhân",
                payload={
                    "productId": 1,
                    "quantity": 1,
                    "productName": target_product["name"],
                    "priceMinor": target_product["price"]
                },
                requires_confirmation=True
            )
        )
        
    # 4. Intent: DISCOVERY & RECOMMENDATION
    matched = search_products(req.message)
    if matched:
        top = matched[0]
        reply_text = (
            f"Dựa trên yêu cầu của bạn, tôi đề xuất: **{top['name']}**.\n\n"
            f"💡 **Điểm nổi bật**: {top['description']}\n"
            f"🏷️ **Thuộc tính AI**: {', '.join(top['tags'])}\n"
            f"💰 **Giá niêm yết**: {top['price']:,} đ"
        )
        return ChatResponse(
            reply=reply_text,
            intent="RECOMMENDATION",
            suggested_products=matched[:3],
            suggested_actions=[
                f"Thêm {top['name'][:20]}... vào giỏ",
                "So sánh với sản phẩm khác",
                "Tư vấn phụ kiện đi kèm"
            ]
        )
        
    # 5. Default General Assistant
    return ChatResponse(
        reply="Chào bạn! Tôi là Trợ lý Mua sắm Thông minh AI-Native Commerce. Tôi có thể hỗ trợ bạn:\n"
              "- 🔍 Tìm kiếm sản phẩm theo nhu cầu tự nhiên (ví dụ: 'laptop mỏng nhẹ pin trâu dưới 35 triệu')\n"
              "- 🛒 Đề xuất cấu hình & thêm nhanh vào giỏ hàng an toàn\n"
              "- 📦 Tra cứu hành trình đơn hàng và chính sách bảo hành, đổi trả\n\n"
              "Bạn đang cần tìm sản phẩm gì hôm nay?",
        intent="GENERAL_FAQ",
        suggested_actions=[
            "Tìm laptop cho sinh viên CNTT",
            "Gợi ý tai nghe chống ồn làm việc",
            "Chính sách đổi trả 7 ngày"
        ]
    )


@app.post("/api/ai/recommend")
def api_recommend(req: RecommendRequest):
    recs = KNOWLEDGE_BASE[:req.limit]
    return {
        "status": "success",
        "count": len(recs),
        "recommendations": recs
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
