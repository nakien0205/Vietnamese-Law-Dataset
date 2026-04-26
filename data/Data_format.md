## Data Format  

### Phải có:

* **doc_type** (string): Một trong 14 loại văn bản pháp luật (link),  đa phần là Hiến Pháp, Bộ Luật, Luật, Nghị Định, Thông Tư. Dùng regex hoặc dùng embedding để so sánh với tiêu đề  
* **doc_name** (string): Tên đầy đủ của văn bản và năm, nếu bỏ dấu được thì lưu theo tên với dấu “_” thay cho khoảng trống. VD: bo_luat_hinh_su_2015
* **doc_num** (string): Số hiệu của văn bản. VD: 86/2025/QH15  
* **issued_date**: Ngày ban hành. Ko nghi rõ, nhưng nó là phần đầu tiên của văn bản, bên phải Số và ghi kiểu *Hà Nội, ngày 27 tháng 11 năm 2015*  
* **effective_date**: Ngày hiệu lực. Nằm ở **ĐIỀU KHOẢN THI HÀNH** ở cuối  
* **validity_status**: Còn hiệu lực (working), Hết hiệu lực (discontinued), Sắp có hiệu lực (applied_soon), Chưa xác định (unknown). Hiện tại chưa có pp xác nhận nên cứ để là unknown.
* **domain** (string): Phân loại luật pháp, cực kì nhiều loại (từ tố tụng, thi hành, trách nhiệm hình sự, quyền dân sự, ...). Phần này cần lập sheet để mỗi đứa tự phân loại riêng nên cứ để trống.
* **doc_id** (string): Điều + doc_name. VD: d156_bo_luat_hinh_su_2015  
* **data**: Lưu theo Điều + Khoản + Điểm a

### Nên có:

* **hierarchy_path** (list[string]): Cấu trúc của pháp luật sẽ có dạng Phần -> Chương -> Mục -> Tiểu Mục (hiếm) -> Điều -> Khoản -> Điểm. Nếu phần nào không có thì bỏ trống. VD: Bộ Luật Dân Sự 2015: ["Phần thứ nhất: Quy Định chung", "Chương III: Cá nhân", "Mục 4: Giám hộ", "Điều 47: Người được giám hộ", "Khoản 1: Người được giám hộ bao gồm", "Điểm c: Người mất năng lực hành vi dân sự"]  
* **cross_references** (list[string]): Các Điều/Khoản khác được nhắc đến. VD: ["d156_bo_luat_hinh_su_2015", "d155_bo_luat_hinh_su_2015"]  
* **url** (string): link cào dữ liệu


### Tính sau:

* **logic_types** (list[string]): Dán nhãn logic để tối ưu hóa tìm kiếm. Tất cả đều là True/False  
  * *definition*: Có phải dùng để giải thích, nêu mục tiêu, ... thay vì nêu pháp luật  
  * *threshold*: Có đề cập đến con số. VD: "Trên 18 tuổi", "Phạt 2.000.000 đồng"  
  * *exception*: Có đề cập đến các ngoại lệ hoặc điều khoản loại trừ trách nhiệm. VD: "Trừ các trường hợp như ABC sẽ miễn tội"  
  * *penalty*: Hình phạt cho vi pham pháp luật. VD: "Ông A do buôn bán chất cấm sẽ bị xử phạt ngồi tù từ 12 năm đến 20 năm"   
  * *procedure*: Thủ tục và quy trình phải thực hiện. VD: "Khi kiểm tra nồng độ cồn, CSGT cần phải chỉ thị người vi phạm thổi hoặc nói vào máy đo không cần ống"  
  * *principle*: Câu mang tính định hướng, tuyên ngôn, không chứa điều kiện hay hình phạt cụ thể. Thường nằm ở các chương đầu của bộ luật. VD: "Mọi người đều bình đẳng trước pháp luật"  
  * *condition*: Các yếu tố định tính bắt buộc phải xảy ra để điều luật được kích hoạt. VD: "Phạm tội có tổ chức", "Lợi dụng chức vụ, quyền hạn"