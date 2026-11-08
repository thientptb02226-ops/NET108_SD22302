namespace AiNativeCommerce.Api.DTOs;

public record LoginRequest(string Email, string Password);
public record RegisterRequest(string Email, string Password, string FullName, string? Phone);
public record LoginResponse(string Token, UserDto User);
public record UserDto(int Id, string Email, string FullName, string? Phone, string Role);

public record AddCartItemRequest(int ProductId, int Quantity);
public record UpdateCartItemRequest(int Quantity);

public record CheckoutRequest(
    string QuoteId,
    string ShippingAddress,
    string ShippingPhone,
    string RecipientName,
    string PaymentMethod
);

public record NlpSearchRequest(string Query);

public record ChatRequest(
    string Message,
    string? SessionId,
    List<ChatMessageDto>? History
);

public record ChatMessageDto(string Role, string Content);

public record ApproveActionRequest(int ActionId, bool Approved);

public record UpdateOrderStatusRequest(string Status);
