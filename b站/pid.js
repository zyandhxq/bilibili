function getPid() {
    var s = "buvid3=810EDA1A-86FC-1091-80E7-8EE19F42B49B03095infoc; b_nut=1682148903; CURRENT_FNVAL=4048; b_lsid=58CEC2D10_187A7E34CD8; _uuid=5BAE1044B-10CE3-9E18-4F88-82E49A34F10A504163infoc; sid=7p19ay7c; buvid_fp=35e43238a06483d34232fcc9a456222a; buvid4=F72A356A-AEC6-B707-319A-69B21302415A57814-023032713-sHvvlqC20wo4bInce2zgGA%3D%3D";
    for (var t = s.split(";"); t.length;) {
        var e = "CURRENT_PID";
        var r = t.pop();
        var n = r.indexOf("=");
        if (n = n < 0 ? r.length : n, decodeURIComponent(r.slice(0, n).replace(/^\s+/, "")) === e) return decodeURIComponent(r.slice(n + 1));
    }
}