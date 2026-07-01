# DANH SÁCH MÀN HÌNH — Module Phân bổ lô hàng & Theo dõi tiến độ chuyển kho

> Mỗi khối khớp 1-1 với placeholder `[[MH-x.y: …]]` trong `_TOBE-BLUEPRINT.md`. Dùng để dựng mockup/giao diện rồi chèn ảnh theo ID. Phần **HƯỚNG DẪN CHUNG** ở đầu áp cho mọi màn hình; chỗ chưa rõ ghi `[CẦN XÁC NHẬN]`.

---

# HƯỚNG DẪN CHUNG CHO AI DỰNG GIAO DIỆN

Phần này là khung dùng chung cho **tất cả** màn hình bên dưới — AI đọc một lần rồi áp cho từng màn, không lặp lại trong mỗi khối.

## 1. Định vị sản phẩm

- **Loại sản phẩm:** Ứng dụng web nội bộ (back-office) cho vận hành kho — không phải website marketing. Ưu tiên **mật độ thông tin cao, thao tác nhanh, bảng dữ liệu lớn**, ít trang trí.
- **Người dùng chính:** 4 vai trò (xem mục 6) — Quản trị hệ thống, Planner MDLZ, Admin FML, Người xem. Đa số thao tác trên màn hình rộng (desktop), độ phân giải ≥ 1366px.
- **Mạch nghiệp vụ (pipeline) là xương sống điều hướng:** Cấu hình nền → Tiếp nhận kế hoạch → Phân bổ → Chốt & tạo đơn → Tích hợp & Theo dõi. Giao diện nên phản ánh đúng mạch này.

## 2. Design system / tokens

- **Màu thương hiệu chủ đạo:** `#176bb4` (xanh Smartlog) — dùng cho thanh điều hướng, nút primary, link, header nhấn.
- **Bảng màu trạng thái** (đề xuất, AI dùng nhất quán):
  - **Thành công / hoàn thành:** xanh lá `#2e9e5b`
  - **Cảnh báo / chờ duyệt:** vàng-cam `#e8a317`
  - **Lỗi / chặn / break-FEFO:** đỏ `#d64545`
  - **Trung tính / nháp / chờ:** xám `#6b7280`
  - **Thông tin / đang xử lý:** xanh dương nhạt `#3b82f6`
- **Font:** Tài liệu (docx) dùng Times New Roman, **nhưng giao diện ứng dụng nên dùng sans-serif** cho dễ đọc trên màn hình — đề xuất **Inter / Roboto / Segoe UI**. `[CẦN XÁC NHẬN nếu khách yêu cầu giữ Times New Roman cho cả UI]`
- **Logo:** dùng `logo-smartlog.png` (góc trái header); `logo-mondelez.png` có thể đặt cạnh để thể hiện đây là hệ cho khách Mondelez.
- **Bo góc:** 6–8px cho card/nút/input. **Mật độ:** bảng dùng mật độ vừa (compact), padding hàng vừa phải để xem được nhiều dòng.

## 3. Khung màn hình dùng chung (app shell)

Mọi màn hình (trừ màn đăng nhập) dùng chung khung:

- **Thanh điều hướng trái (sidebar):** gom theo pipeline, có icon + nhãn. Đề xuất nhóm menu:
  - **Cấu hình nền:** Danh mục kho (MH-2.1) · Master data SKU (MH-2.2) · Quy tắc & ngưỡng (MH-2.3) · Nguồn lấy hàng theo luồng (MH-2.4) · Mẫu file kế hoạch (MH-3.1)
  - **Tiếp nhận kế hoạch:** Tải lên & xem trước (MH-3.2)
  - **Phân bổ:** Kết quả phân bổ (MH-4.1) · Phân bổ theo luồng & nguồn (MH-4.2) · Duyệt hạn dùng (MH-4.3)
  - **Chốt & Đơn:** Danh sách đơn TO (MH-5.1) · Dòng soạn theo lộ trình (MH-5.2) · Theo dõi tích hợp (MH-5.3)
  - **Theo dõi tiến độ:** Dashboard Plan vs Actual (MH-5.5)
- **Header trên cùng:** logo + tên module · breadcrumb · tên/role người đăng nhập · chuông thông báo (đơn lỗi, cảnh báo chờ xử lý).
- **Vùng nội dung chính:** tiêu đề màn hình + (nếu có) thanh bộ lọc + bảng/form.
- **Ngôn ngữ:** **Tiếng Việt** toàn bộ. Số lượng tách nghìn bằng dấu chấm (vd 21.600); ngày giờ định dạng `DD/MM/YYYY HH:mm`.

## 4. Component dùng chung (tái sử dụng giữa các màn)

- **Bảng dữ liệu (data table):** sắp xếp theo cột, lọc, phân trang, cố định header khi cuộn; hàng có thể **bung (expand)** để xem dòng con (vd đơn → dòng đơn, dòng kế hoạch → các lô phân bổ).
- **Chip trạng thái:** dùng bảng màu mục 2 (vd "Đã chốt & khóa" = xanh lá, "Chờ duyệt" = vàng, "Lỗi tích hợp" = đỏ).
- **Cờ break-FEFO:** badge đỏ nổi bật + tooltip giải thích ("lấy từ kho xuất bán BKD1 dự phòng — phá nguyên tắc hạn dùng").
- **Panel cảnh báo:** vùng gom cảnh báo cần xử lý ở đầu màn (thiếu tồn / lô chỉ định không đủ / break-FEFO chờ duyệt), bấm vào nhảy tới dòng tương ứng.
- **Thanh bộ lọc (filter bar):** lọc theo Luồng (In-In / In-Ex), Nhánh (BKD / NKD), Ngày kế hoạch, Kho — dùng lại ở MH-4.x, 5.x.
- **Nút hành động chính (primary):** chỉ **một** nút primary nổi bật mỗi màn (Phân bổ / Chốt / Xuất báo cáo…); nút phụ dùng style outline.

## 5. Trạng thái bắt buộc xử lý cho MỌI màn hình

AI luôn thiết kế đủ các state sau (đừng chỉ vẽ trạng thái "có dữ liệu đẹp"):

- **Rỗng (empty):** chưa có dữ liệu — kèm hướng dẫn bước kế tiếp.
- **Đang tải (loading):** skeleton/spinner, nhất là màn gọi WMS qua API.
- **Lỗi (error):** gọi API thất bại, file sai — thông báo rõ + nút thử lại.
- **Theo quyền:** ẩn/khóa nút theo vai trò (mục 6) — vd Người xem chỉ thấy nút Xuất báo cáo.
- **Chỉ đọc (read-only):** dữ liệu đã khóa (phương án đã chốt) hiển thị mờ, không cho sửa.

## 6. Phân quyền hiển thị (theo mục 7 blueprint)

Giao diện phải tôn trọng ma trận quyền — nút/thao tác ẩn hoặc disable theo vai trò:

| Vai trò | Thấy & làm được |
|---|---|
| **Quản trị hệ thống** | Toàn quyền các màn Cấu hình nền (MH-2.x, 3.1); xem phần còn lại |
| **Planner MDLZ** | Tải kế hoạch (MH-3.2); duyệt cổng hạn dùng (MH-4.3); theo dõi & xuất báo cáo (MH-5.5) |
| **Admin FML** | Xử lý lỗi tích hợp / hủy-tạo lại đơn (MH-5.3); theo dõi & xuất báo cáo |
| **Người xem** | Chỉ xem Dashboard & báo cáo (MH-5.5), không thao tác |

> Phân vai mặc định gán lại được qua cấu hình (mục 7 blueprint); UI nên đọc quyền động, không hard-code.

## 7. Nguyên tắc thiết kế xuyên suốt

- **Truy vết & giải thích:** ở các màn phân bổ/chốt, mỗi lô được chọn phải xem được **lý do** (theo chiến thuật FEFO/LEFO/Nhập xưởng/Chỉ định batch).
- **Tách bạch hệ thống vs thực tế:** ở Dashboard, làm rõ "hoàn thành theo hệ thống (đã xuất)" khác "Complete thực tế (đã lên kệ)" — đừng để con số gây hiểu nhầm.
- **Không cho đi tiếp khi còn lỗi chặn:** nút primary (Phân bổ / Chốt) chỉ **bật** khi hết cảnh báo chặn.
- **Hành động khó đảo ngược (chốt, hủy đơn, tích hợp lại):** luôn có bước xác nhận.

---

# DANH SÁCH MÀN HÌNH

### [[MH-2.1: Màn hình Danh mục kho & cấu hình theo kho]]
- **Hệ thống / nền tảng:** Module — Web (cấu hình/quản trị). Vai trò: Quản trị hệ thống (C R U D); các vai khác chỉ xem.
- **Mục đích màn hình:** Khai báo các kho tham gia chuyển kho cùng thuộc tính cố định của từng kho: mã, tên, cụm, **loại kho (Kho trong / Kho ngoài)**, danh sách trạng thái (`STATUS`) được phép lấy theo kho, và zone trung chuyển (put-away) theo kho. **Lưu ý:** vai trò *Nguồn/Đích* là **theo luồng, không khai ở màn này** (nguồn khai ở MH-2.4, đích lấy từ cột Kho đích của kế hoạch).
- **Bố cục tổng thể:** Header + nút "Thêm kho"; bảng danh sách kho bên trái; form/tab chi tiết kho bên phải (hoặc popup) gồm các tab phụ: *Thông tin chung*, *Trạng thái lấy được (whitelist STATUS)*, *Zone trung chuyển*.
- **Thành phần & trường chính:**
  - **Bảng danh sách kho** — cột: Mã kho, Tên kho, Cụm, Loại kho (Kho trong / Kho ngoài), Thao tác (sửa/xóa).
  - **Tab Whitelist STATUS** — bảng ánh xạ một-nhiều: Mã kho × các giá trị `STATUS` được lấy chuyển kho (vd BKD1 = `0001_OK`); kho không khai = lấy tất cả.
  - **Tab Zone trung chuyển** — bảng Mã kho × Zone trung chuyển (`PUTAWAYZONE`, vd BKD1 = `STAGE`); một kho có thể nhiều dòng.
  - Nút Lưu, Xóa.
- **Trạng thái / biến thể:** Danh sách rỗng (chưa khai kho); cảnh báo trùng mã kho; kho chưa khai whitelist (ghi chú "lấy tất cả trạng thái").
- **Gợi ý thiết kế:** Bảng mật độ vừa; làm nổi cột Loại kho & Cụm bằng chip màu; tách 3 tab cho rõ (thuộc tính / trạng thái / zone).
- **Tham chiếu nghiệp vụ:** mục 2.1. _(Truy vết: BR-031, BR-008, BR-013, BR-023; BRULE-01/03/04; OQ-09/11/12.)_

### [[MH-2.2: Màn hình Master data SKU (đơn vị & quy đổi)]]
- **Hệ thống / nền tảng:** Module — Web. Dữ liệu **tải lên bằng Excel, độc lập với WMS** (không đồng bộ danh mục SKU từ WMS). Vai trò: Quản trị hệ thống (C R U D).
- **Mục đích màn hình:** Quản lý bộ **đơn vị & hệ số quy đổi** (PCS ↔ CASE ↔ PALLET) cho từng SKU để hệ thống quy đổi số lượng nhất quán khi phân bổ và hiển thị tiến độ. **Lưu ý:** màn này **KHÔNG** chứa tồn/% hạn dùng (tồn lấy từ WMS lúc phân bổ) và **không** chứa trạng thái lấy hàng (trạng thái khai theo kho ở MH-2.1).
- **Bố cục tổng thể:** Nút "Tải lên Excel" + "Tải file mẫu" trên cùng; thanh tìm kiếm SKU; bảng danh sách SKU; form xem/sửa một SKU.
- **Thành phần & trường chính:**
  - **Bảng SKU** — cột: Mã hàng (khớp mã WMS), Tên hàng, Đơn vị nhỏ nhất (PCS), Đơn vị cấp hộp (CASE), Số lượng quy đổi cấp hộp (1 CASE = ? PCS), Đơn vị cấp pallet (PALLET), Số lượng quy đổi cấp pallet (1 PALLET = ? PCS).
  - Nút Tải lên Excel (kèm xem trước & báo dòng lỗi), Tải file mẫu.
- **Trạng thái / biến thể:** SKU thiếu quy cách (cảnh báo thiếu hệ số quy đổi cấp pallet → không nở được pallet); file Excel sai cấu trúc khi tải lên (liệt kê dòng lỗi).
- **Gợi ý thiết kế:** Nhấn mạnh cặp (đơn vị + số lượng quy đổi) theo từng cấp; dữ liệu chủ yếu read-only sau khi tải, sửa qua tải lại file hoặc sửa lẻ.
- **Tham chiếu nghiệp vụ:** mục 2.2. _(Truy vết: BR-007, BR-008; BRULE-03/11.)_

### [[MH-2.3: Màn hình Cấu hình quy tắc phân bổ & ngưỡng vận hành]]
- **Hệ thống / nền tảng:** Module — Web (cấu hình/quản trị). Vai trò: Quản trị hệ thống (C R U D). **Lưu ý:** việc **gán vai trò cho từng bước KHÔNG ở màn này** — phân quyền nằm ở mục 7 (cấu hình phân quyền riêng).
- **Mục đích màn hình:** Tham số hóa các ngưỡng & cổng duyệt vận hành để đổi chính sách không phải sửa hệ thống.
- **Bố cục tổng thể:** Form tham số chia nhóm: *Phân bổ & tách đơn* / *Cổng duyệt* / *Theo dõi*; mỗi tham số kèm dòng giải thích ngắn; nút Lưu.
- **Thành phần & trường chính:**
  - Trường số **"Ngưỡng pallet tối đa mỗi đơn"** (mặc định 100) — vượt thì tự tách đơn.
  - Công tắc **"Cổng duyệt kiểm soát hạn dùng (break-FEFO, In-Ex BKD)"** (mặc định Bật).
  - Công tắc **"Bước duyệt/chốt phương án trước khi tạo đơn"** (mặc định Bật; tắt ⇒ hệ thống tự chốt).
  - (Tùy chọn) Ngưỡng số ngày cho chiến thuật **"Nhập xưởng"** `[CẦN XÁC NHẬN — OQ-10]`; sức chứa đơn theo khu (khu hàng pallet/thùng chẵn · khu nhặt lẻ · đơn vị tính sức chứa) cho tối ưu tuyến soạn.
- **Trạng thái / biến thể:** Cảnh báo khi nhập ngưỡng ngoài khoảng hợp lệ; mỗi công tắc kèm hệ quả ("tắt ⇒ bỏ cổng duyệt").
- **Gợi ý thiết kế:** Dạng form "Tên tham số — giá trị — giải thích"; công tắc bật/tắt rõ ràng (toggle); không trộn phần phân quyền vào đây.
- **Tham chiếu nghiệp vụ:** mục 2.3. _(Truy vết: BR-031, BR-009, BR-015, BR-029, BR-025; BRULE-02.)_

### [[MH-2.4: Màn hình Cấu hình nguồn lấy hàng theo luồng]]
- **Hệ thống / nền tảng:** Module — Web (cấu hình/quản trị). Vai trò: Quản trị hệ thống (C R U D).
- **Mục đích màn hình:** Khai báo **tường minh** quy tắc "lấy kho nào trước, xét chung những kho nào" theo từng tổ hợp (Luồng × Cụm kho nguồn), thành nhiều **bậc lấy** có thứ tự — thay cho việc nằm trong trí nhớ nhân viên.
- **Bố cục tổng thể:** Bảng cấu hình nhóm theo (Luồng × Cụm kho nguồn); mỗi nhóm liệt kê các bậc theo thứ tự; nút Thêm bậc / Thêm dòng; nút Lưu.
- **Thành phần & trường chính:**
  - **Bảng bậc lấy** — cột: Luồng (In-In / In-Ex), Cụm kho nguồn (giá trị Cụm khai ở MH-2.1, vd BKD/NKD), Bậc lấy (số, nhỏ trước), Các kho lấy ở bậc này (multi-select — nhiều kho = xét chung lô).
  - Cấu hình mặc định mẫu: In-In/BKD bậc 1 = {BKD2, BKD3}; In-Ex/BKD bậc 1 = {BKD2, BKD3}, bậc 2 (dự phòng) = {BKD1}; In-Ex/NKD bậc 1 = {NKD}.
- **Trạng thái / biến thể:** Cảnh báo nếu kho đích bị khai làm nguồn (kho không thể vừa nguồn vừa đích); ghi chú "bậc dự phòng BKD1 sẽ kích hoạt cổng duyệt break-FEFO".
- **Gợi ý thiết kế:** Hiển thị trực quan thứ tự bậc (1 → 2 → …) như các bước; đánh dấu bậc dự phòng BKD1 bằng badge cảnh báo; ghi chú "nhiều kho cùng bậc = xét chung, không lấy cạn kho nào trước".
- **Tham chiếu nghiệp vụ:** mục 2.4. _(Truy vết: BR-004, BR-005, BR-029, BR-030; BRULE-01/04.)_

### [[MH-3.1: Màn hình cấu hình mẫu file kế hoạch (định nghĩa cột)]]
- **Hệ thống / nền tảng:** Module — Web (cấu hình/quản trị). Vai trò: Quản trị sửa được; người dùng thường chỉ đọc.
- **Mục đích màn hình:** Khai báo/đối chiếu cấu trúc cột chuẩn của file kế hoạch để hệ thống đọc đúng; tải xuống file mẫu.
- **Bố cục tổng thể:** Bảng danh sách cột template; nút "Tải file mẫu".
- **Thành phần & trường chính:** Bảng cột (Tên cột, Kiểu dữ liệu, Bắt buộc, Mô tả) theo mục 3.3 — gồm: Luồng chuyển kho, Cụm kho nguồn, Kho đích, Mã hàng (SKU), Số lượng pallet, Nguyên tắc phân bổ (FEFO/LEFO/Nhập xưởng/Chỉ định batch), Batch chỉ định (có điều kiện); nút "Tải file mẫu".
- **Trạng thái / biến thể:** Chỉ đọc với người dùng thường; sửa được với quản trị.
- **Gợi ý thiết kế:** Đánh dấu rõ cột bắt buộc; ghi chú cột có điều kiện (Batch chỉ điền khi Nguyên tắc = Chỉ định batch).
- **Tham chiếu nghiệp vụ:** mục 3.3. _(Truy vết: BR-001, BR-006; AS-01, NFR-08.)_

### [[MH-3.2: Màn hình tải lên & xem trước file kế hoạch]]
- **Hệ thống / nền tảng:** Module — Web. Vai trò: Planner MDLZ (C R U D kế hoạch).
- **Mục đích màn hình:** Tải lên file Excel kế hoạch, kiểm tra hợp lệ, nhận diện luồng/nhánh và xem trước trước khi phân bổ.
- **Bố cục tổng thể:** Vùng kéo-thả/chọn file + nút Tải lên; bảng xem trước các dòng kế hoạch; vùng cảnh báo lỗi cấu trúc/định dạng; nút "Phân bổ".
- **Thành phần & trường chính:**
  - Nút chọn file (kéo-thả).
  - **Bảng xem trước** — cột theo template (Luồng, Cụm kho nguồn, Kho đích, SKU, Số pallet, Nguyên tắc phân bổ, Batch) + cột hệ thống tự gắn: **Luồng nhận diện** (In-In/In-Ex) và **Nhánh** (BKD/NKD).
  - **Danh sách lỗi** — liệt kê dòng/cột sai (thiếu cột bắt buộc, SKU không có trong master, số pallet không phải số nguyên dương, mã kho lạ, dòng Chỉ định batch nhưng trống Batch).
  - Nút "Phân bổ" (chỉ bật khi không còn lỗi).
- **Trạng thái / biến thể:** File đúng cấu trúc (cho phân bổ); file sai (chặn, liệt kê lỗi); file rỗng; đang kiểm tra (loading).
- **Gợi ý thiết kế:** Tô đỏ ô lỗi & cho nhảy tới dòng lỗi; nút Phân bổ disable khi còn lỗi; hiển thị tổng số dòng hợp lệ/lỗi.
- **Tham chiếu nghiệp vụ:** mục 3.4. _(Truy vết: BR-001, BR-002, BR-006; NFR-03/08; EX-06.)_

### [[MH-3.5: Màn hình Tồn kho WMS (đồng bộ & tra cứu tồn theo lô)]]
- **Hệ thống / nền tảng:** Module — Web. Vai trò: Admin FML / Planner MDLZ (R + bấm đồng bộ tay); hệ thống tự đồng bộ định kỳ.
- **Mục đích màn hình:** Hiển thị bản tồn đồng bộ từ WMS (nguồn tồn cho phân bổ ở mục 4); cho đồng bộ tự động 15 phút/lần hoặc thủ công, và tra cứu tồn theo SKU / lô / vị trí / trạng thái.
- **Bố cục tổng thể:** Thanh đồng bộ trên cùng (mốc đồng bộ lần cuối · công tắc tự động 15 phút · nút đồng bộ tay có spinner) + thẻ tổng hợp (tổng pallet · tổng SKU · số lô cận hạn) + thanh bộ lọc (tìm SKU/tên, lọc trạng thái) + bảng tồn theo lô.
- **Thành phần & trường chính:**
  - **Thanh đồng bộ** — "Đồng bộ lần cuối: DD/MM/YYYY HH:mm" (chấm xanh), công tắc **Tự động 15 phút** (bật/tắt), nút **Đồng bộ ngay** (đang đồng bộ → spinner ~1.5s rồi cập nhật mốc).
  - **Bảng tồn** — cột: Kho, Mã hàng (SKU), Tên hàng, Mã lô (`LOTTABLE01`), Vị trí (Dãy.Bay.Tầng), Pallet ID, Trạng thái (`STATUS`), Số pallet, **Khả dụng** (0 nếu trạng thái không cho lấy), **% hạn dùng còn lại** (thanh màu: đỏ <35 · vàng <60 · xanh), Ngày nhận.
  - **Thẻ tổng hợp** — tổng pallet · tổng SKU · số lô cận hạn (% hạn dùng thấp).
  - **Chip trạng thái** theo bảng màu: OK/0001_OK = xanh (khả dụng); EXPORT = xanh dương; GTDC/HOLD = vàng; BLOCKED/EXPIRED/DAMAGE = đỏ (khả dụng = 0).
- **Trạng thái / biến thể:** Có dữ liệu; đang đồng bộ (spinner + disable nút); đồng bộ lỗi (thông báo + nút thử lại); rỗng (chưa đồng bộ lần nào); lọc không có kết quả.
- **Gợi ý thiết kế:** Nêu rõ độ tươi dữ liệu (mốc đồng bộ lần cuối) để người dùng biết nên đồng bộ tay trước khi phân bổ; đánh dấu lô cận hạn nổi bật; dòng khả dụng = 0 làm mờ.
- **Tham chiếu nghiệp vụ:** mục 3.5, 4.1. _(Truy vết: BR-007, BR-008, BR-011; NFR-04; OQ-11.)_

### [[MH-4.1: Màn hình kết quả phân bổ batch — tách theo kho lấy hàng, đơn TO & chi tiết TO]]
- **Hệ thống / nền tảng:** Module — Web (chức năng Phân bổ). Phân bổ là **đề xuất tự động của hệ thống** (chưa phải lệnh thực thi — cần duyệt mới chuyển tích hợp).
- **Mục đích màn hình:** Sau khi chạy phân bổ, hiển thị kết quả **đã tách sẵn theo kho lấy hàng (kho nguồn) và gom thành đơn chuyển kho (TO) kèm chi tiết từng dòng** — người dùng thấy ngay mỗi dòng kế hoạch lấy ở kho nào, thành những đơn TO nào, và đọc được **vì sao mỗi lô được chọn**.
- **Bố cục tổng thể:** Thanh bộ lọc (Luồng / Chiến thuật / Kho); bảng kết quả phân bổ phân cấp 3 mức — **Kho lấy hàng → đơn TO → dòng chi tiết TO**.
- **Thành phần & trường chính:**
  - **Bảng phân bổ phân cấp** — cấp 1 = nhóm theo **Kho lấy hàng (kho nguồn)**; cấp 2 = **đơn TO** (mã SO, kho nguồn → kho đích, tổng pallet, cờ cảnh báo của đơn); cấp 3 = **dòng chi tiết TO**: Mã hàng (SKU), Mã lô (`LOTTABLE01`), Số pallet phân bổ, Số lượng (PCS), % hạn dùng còn lại, Cờ cảnh báo.
  - **Cờ cảnh báo:** thiếu tồn / lô chỉ định không đủ / break-FEFO (gắn ở Lưu đồ A, mục 4.1).
  - Hiển thị "X pallet + Y PCS lẻ" khi lô góp phần lẻ.
- **Trạng thái / biến thể:** Dòng đủ tồn (bình thường); dòng thiếu tồn (badge đỏ); dòng có lô chỉ định không khả dụng; dòng/đơn mang cờ break-FEFO chờ duyệt; đang gọi WMS (loading).
- **Gợi ý thiết kế:** Tooltip/ghi chú giải thích thứ tự chọn lô theo chiến thuật (FEFO = % hạn dùng tăng dần…); cờ cảnh báo nổi bật ở cấp đơn TO; nút **Duyệt** để chốt phương án (cổng break-FEFO ở MH-4.3) rồi chuyển tích hợp WMS.
- **Tham chiếu nghiệp vụ:** mục 4.1, 5.1. _(Truy vết: BR-003, BR-006→009, BR-013, BR-014, BR-015; BRULE-01/03/11; OQ-10.)_

### [[MH-4.2: Màn hình phân bổ theo luồng & nguồn lấy hàng]]
- **Hệ thống / nền tảng:** Module — Web (cùng chức năng Phân bổ với MH-4.1, góc nhìn theo bậc nguồn).
- **Mục đích màn hình:** Hiển thị mỗi dòng phân bổ kèm **bậc lấy** và **kho nguồn**, cho thấy phần nào lấy từ bậc chính, phần nào chạm bậc dự phòng BKD1 (kèm cờ break-FEFO).
- **Bố cục tổng thể:** Thanh bộ lọc (Luồng / Nhánh); bảng phân bổ **nhóm theo bậc lấy** (bậc 1 → bậc dự phòng).
- **Thành phần & trường chính:**
  - **Bảng phân bổ theo bậc** — cột: Dòng kế hoạch, Luồng/Nhánh, Bậc lấy (1 / 2 dự phòng), Kho lấy, Mã lô, Số pallet, Cờ break-FEFO (chờ duyệt / đã duyệt).
  - Nhóm trực quan: bậc 1 (xét chung các kho) vs bậc dự phòng BKD1.
- **Trạng thái / biến thể:** Chỉ một bậc (In-In, In-Ex/NKD — không có dự phòng); có chạm bậc dự phòng BKD1 (hiện cờ break-FEFO); thiếu tồn sau khi hết bậc.
- **Gợi ý thiết kế:** Phân tách rõ "bậc chính" và "bậc dự phòng"; phần lấy từ BKD1 tô cảnh báo; giải thích "xét chung lô của các kho trong cùng bậc".
- **Tham chiếu nghiệp vụ:** mục 4.1 (Lưu đồ A). _(Truy vết: BR-004, BR-005, BR-029, BR-030; BRULE-01/04; OQ-09/19.)_

### [[MH-4.3: Màn hình duyệt cổng kiểm soát hạn dùng (break-FEFO)]]
- **Hệ thống / nền tảng:** Module — Web. Vai trò duyệt: Planner MDLZ (mặc định; gán lại được). Chỉ xuất hiện khi cổng đang Bật (MH-2.3) và có dòng chạm bậc dự phòng BKD1.
- **Mục đích màn hình:** Cho người có thẩm quyền **đối chiếu hạn dùng** lô BKD1 dự phòng với tồn bậc trên rồi **xác nhận** hoặc **từ chối** việc phá nguyên tắc FEFO.
- **Bố cục tổng thể:** Danh sách các dòng mang cờ break-FEFO; mỗi dòng có vùng đối chiếu hạn dùng (BKD1 vs bậc trên) + nút Xác nhận / Từ chối.
- **Thành phần & trường chính:**
  - **Danh sách dòng break-FEFO** — cột: Dòng kế hoạch, SKU, Lô BKD1, Số pallet lấy từ BKD1, % hạn dùng lô BKD1, % hạn dùng tham chiếu của bậc trên, Trạng thái duyệt.
  - Nút **Xác nhận** (cho lấy) / **Từ chối** (coi như thiếu tồn → ngoại lệ EX-04).
  - Ô ghi chú lý do duyệt/từ chối (truy vết).
- **Trạng thái / biến thể:** Không có dòng nào (cổng tắt hoặc không chạm BKD1 — màn ẩn/empty); chờ duyệt; đã duyệt; đã từ chối.
- **Gợi ý thiết kế:** Làm nổi chênh lệch % hạn dùng (BKD1 thấp hơn ⇒ cảnh báo); thao tác duyệt cần xác nhận; có thể nhúng ngay trong panel cảnh báo của MH-4.1.
- **Tham chiếu nghiệp vụ:** mục 4.1 (Bước 3). _(Truy vết: BR-029, BR-030; BRULE-04; OQ-19; EX-04.)_

### [[MH-5.1: Màn hình danh sách đơn chuyển kho (TO) đã tạo]]
- **Hệ thống / nền tảng:** Module — Web. Đơn TO **do hệ thống tự sinh** sau khi chốt phương án (không tạo tay).
- **Mục đích màn hình:** Hiển thị các đơn TO vừa tạo (tách theo kho nguồn × kho đích × ngưỡng pallet), mỗi đơn mang mã SO dùng chung; cho kiểm tra trước khi/đang tích hợp.
- **Bố cục tổng thể:** Thanh bộ lọc (Luồng / Kho / Trạng thái); bảng đơn TO theo mã SO; hàng đơn bung ra các dòng đơn.
- **Thành phần & trường chính:**
  - **Bảng đầu đơn** — cột: Mã đơn (SO), Loại đơn (ORDER TYPE) `[CẦN XÁC NHẬN — OQ-16]`, Luồng/Nhánh, Kho nguồn, Kho đích, Tổng số pallet (≤ ngưỡng MH-2.3), Trạng thái đơn (Đã tạo / Đã tích hợp / Lỗi), Tham chiếu phương án (PA).
  - **Bảng dòng đơn (bung)** — cột: Mã SO, SKU, Mã lô, Số pallet, Số lượng (PCS), Vị trí lấy gợi ý (nếu có, từ MH-5.2).
- **Trạng thái / biến thể:** Đơn vừa tạo (Đã tạo); đang tích hợp; đã tích hợp; lỗi tích hợp; đơn bị tách do vượt ngưỡng pallet (nhóm nhiều SO).
- **Gợi ý thiết kế:** Chip trạng thái theo màu; nhóm các đơn cùng phương án; chỉ rõ đơn nào bị tách từ một nhóm vượt ngưỡng.
- **Tham chiếu nghiệp vụ:** mục 5.2.1. _(Truy vết: BR-014, BR-015, BR-032; BRULE-02; OQ-16.)_

### [[MH-5.2: Màn hình dòng soạn theo lộ trình & vị trí lấy hàng của đơn]]
- **Hệ thống / nền tảng:** Module — Web. Áp cho kho nguồn **có dữ liệu trường `ORDER`** (số thứ tự lối đi soạn) trong danh mục vị trí (đã kiểm chứng cho BKD1); kho chưa có thì bỏ qua, đơn giữ thứ tự nền.
- **Mục đích màn hình:** Hiển thị các dòng soạn của một đơn TO đã **sắp theo lộ trình soạn** (`ORDER` tăng dần) để gom SKU gần nhau & rút ngắn tuyến soạn; thể hiện vị trí lấy hàng được chọn khi một lô nằm nhiều vị trí.
- **Bố cục tổng thể:** Header đơn (mã SO, kho nguồn); bảng dòng soạn sắp theo `ORDER`, **nhóm theo dãy**; chỉ báo sức chứa đơn theo khu.
- **Thành phần & trường chính:**
  - **Bảng dòng soạn** — cột: Thứ tự (`ORDER`), Mã vị trí (Dãy.Bay.Tầng, vd A17.13.2), SKU, Mã lô, Số pallet, Vị trí lấy hàng đã chọn.
  - Nhóm theo dãy; chỉ báo cắt đơn theo sức chứa khu (khu hàng pallet/thùng chẵn · khu nhặt lẻ).
  - Ghi chú: lô đã chọn theo chiến thuật là **ràng buộc cứng**, tối ưu tuyến không đổi lô.
- **Trạng thái / biến thể:** Kho có dữ liệu `ORDER` (hiển thị lộ trình); kho không có dữ liệu (ẩn lộ trình, thông báo "không áp tối ưu vị trí"); vị trí bị loại (đang kiểm kê, đang khóa, vị trí rác).
- **Gợi ý thiết kế:** Trực quan hóa tuyến đi theo thứ tự `ORDER`; phân nhóm dãy bằng header phụ; có thể minh họa sơ đồ kho đơn giản (tùy chọn).
- **Tham chiếu nghiệp vụ:** mục 5.2.2. _(Truy vết: BR-017, BR-018; OQ-15.)_

### [[MH-5.3: Màn hình theo dõi tích hợp đơn xuống WMS]]
- **Hệ thống / nền tảng:** Module — Web. Tích hợp **tự động qua API** (In-In & In-Ex chung kênh, không qua SAP). Vai trò xử lý lỗi: Admin FML.
- **Mục đích màn hình:** Theo dõi trạng thái tích hợp từng đơn TO xuống WMS, lấy về ORDER KEY, và xử lý đơn lỗi (tích hợp lại / hủy–tạo lại).
- **Bố cục tổng thể:** Thanh bộ lọc (Trạng thái tích hợp / Luồng / Kho); bảng đơn theo mã SO với cột tích hợp; vùng/tab "Đơn lỗi" riêng.
- **Thành phần & trường chính:**
  - **Bảng tích hợp** — cột: Mã kế hoạch (Plan), Mã đơn (SO), ORDER KEY (WMS cấp), Luồng/Nhánh, Trạng thái tích hợp (Chờ / Đã tích hợp / Lỗi), Thời điểm tích hợp.
  - Nút **Tích hợp lại** (chống trùng theo SO) cho đơn lỗi; nút **Hủy & tạo lại** khi cần sửa đơn đã tích hợp.
  - Phân biệt rõ: *ORDER KEY* (khóa đơn WMS) khác trường *`ORDER`* (số thứ tự lối đi soạn ở MH-5.2).
- **Trạng thái / biến thể:** Chờ tích hợp; đang retry; đã tích hợp (có ORDER KEY); lỗi tích hợp (hết lượt retry — vào tab lỗi); đơn bị hủy–tạo lại.
- **Gợi ý thiết kế:** Chip trạng thái màu; đơn lỗi nổi bật + lý do lỗi; thao tác hủy/tạo lại cần xác nhận; hiển thị chuỗi liên kết Plan ↔ SO ↔ ORDER KEY.
- **Tham chiếu nghiệp vụ:** mục 5.3. _(Truy vết: BR-016, BR-019, BR-020; NFR-03; EX-05; OQ-16.)_

### [[MH-5.5: Màn hình Dashboard theo dõi tiến độ Plan vs Actual]]
- **Hệ thống / nền tảng:** Module — Web. Nền dữ liệu **tự đồng bộ từ WMS ~15 phút/lần** (không qua SAP). Vai trò: Admin FML / Planner MDLZ (xem + xuất báo cáo); Người xem (chỉ xem). _(Giữ số MH-5.5 cho Dashboard; MH-5.4 để trống — khớp đánh số trong blueprint.)_
- **Mục đích màn hình:** Một dashboard chung đối soát **kế hoạch vs thực tế**, **tách hàng đã lên kệ với hàng còn ở khu trung chuyển (Stage Transfer)** để phản ánh đúng tiến độ; thay báo cáo Zalo thủ công.
- **Bố cục tổng thể:** Thanh bộ lọc (Luồng / Nhánh / Ngày kế hoạch / Kho); thẻ KPI tổng (Plan / Complete thực tế / Pending / %); **bảng Plan vs Actual** là phần lõi; vùng Stage Transfer & thời gian lưu; nút Xuất báo cáo.
- **Thành phần & trường chính:**
  - **Bảng Plan vs Actual** — **tập cột khác nhau theo luồng**:
    - **In-In:** Plan · Đã xuất (= hoàn thành theo hệ thống, gồm cả Stage Transfer) · Stage Transfer · **Complete thực tế (= Đã xuất − Stage Transfer)** · Pending · % hoàn thành.
    - **In-Ex:** Plan · Đã xuất · **Complete (= Đã xuất)** · Pending · % hoàn thành (không có Stage Transfer / Complete thực tế).
  - **Cột Stage Transfer (chỉ In-In)** kèm **thời gian hàng đã nằm** ở khu trung chuyển → cảnh báo tồn đọng.
  - Mọi số cộng dồn theo **PCS**, hiển thị quy đổi **pallet**.
  - Nút **Xuất báo cáo** (breakdown theo pallet/trạng thái) để tải về/chia sẻ.
- **Trạng thái / biến thể:** Đang đồng bộ / vừa làm tươi (hiện mốc thời gian cập nhật gần nhất); pallet kẹt lâu ở Stage Transfer (cảnh báo); In-In vs In-Ex hiển thị bộ cột khác nhau; không có dữ liệu (empty).
- **Gợi ý thiết kế:** **Làm rõ "đã xuất 80% ≠ hoàn thành 80%"** — nhấn mạnh Complete thực tế; thanh tiến độ kép (đã xuất vs đã lên kệ); ghi chú vì sao In-Ex ngắn hơn (kho ngoài không trên WMS của FML); hiển thị mốc đồng bộ gần nhất.
- **Tham chiếu nghiệp vụ:** mục 5.4. _(Truy vết: BR-021→028, BR-033; NFR-04; BRULE-09/10; OQ-13/20.)_

---

> **Lưu ý cho AI:** Các điểm `[CẦN XÁC NHẬN]` / mã `OQ-xx` là tham số chờ Mondelez/FML chốt (xem mục 8 blueprint) — khi dựng UI cứ để dạng trường cấu hình/placeholder, không hard-code giá trị.
