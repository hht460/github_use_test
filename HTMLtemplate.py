
html_result_str = '''
<!DOCTYPE html>
<html>
<head>
<title></title>
<style type="text/css">
body,table{
font-size:20px;
}
table{
empty-cells:show;
border-collapse: collapse;
margin:0 auto;
}
td{
height:30px;
}
h1,h2,h3{
font-size:20px;
margin:0;
padding:0;
}
.table{
border:1px solid #cad9ea;
color:#666;
}
.table th {
background-repeat:repeat-x;
height:30px;
}
.table td,.table th{
border:1px solid #cad9ea;
padding:0 1em 0;
}
.table tr.alter{
background-color:#f5fafe;
}
</style>
</head>
<body>
<div align="center">
<h1 align="center"> TEST RESULT REPORT </h1>
<hr />
</div>

<div>
<table border="1" width="70%" align="center" bgcolor=rgb(233,233,233)>
<tbody>
<tr>
    <td align="center" rowspan="7">test_info</td>
    <td align="center">product_name</td>
    <td align="center" colspan="2">json_product_name</td>
</tr>
<tr>
    <td align="center">test_name</td>
    <td align="center" colspan="2">json_test_name</td>
</tr>
<tr>
    <td align="center">sal_version</td>
    <td align="center" colspan="2">json_sal_version</td>
</tr>
<tr>
    <td align="center">sal_pattern_version</td>
    <td align="center" colspan="2">json_sal_pattern_version</td>
</tr>
<tr>
    <td align="center">bep_version</td>
    <td align="center" colspan="2">json_bep_version</td>
</tr>
<tr>
    <td align="center">bep_pattern_version</td>
    <td align="center" colspan="2">json_bep_pattern_version</td>
</tr>
<tr>
    <td align="center">result_path</td>
    <td align="center" colspan="2">json_result_path</td>
</tr>
<tr>
    <td align="center" rowspan="20">test_result</td>
    <td align="center" rowspan="5">flash</td>
    <td align="center">total</td>
    <td align="center">json_flash_total_sample</td>
</tr>
<tr>
    <td align="center">malicious</td>
    <td align="center">json_flash_malicious_sample</td>
</tr>
<tr>
    <td align="center">monitoring</td>
    <td align="center">json_flash_monitoring_sample</td>
</tr>
<tr>
    <td align="center">undetermined</td>
    <td align="center">json_flash_undetermined_sample</td>
</tr>
<tr>
    <td align="center">malicious_rate</td>
    <td align="center"><b>json_flash_malicious_rate_sample</b></td>
</tr>
<tr>
    <td align="center" rowspan="5">html</td>
    <td align="center">total</td>
    <td align="center">json_html_total_sample</td>
</tr>
<tr>
    <td align="center">malicious</td>
    <td align="center">json_html_malicious_sample</td>
</tr>
<tr>
    <td align="center">monitoring</td>
    <td align="center">json_html_monitoring_sample</td>
</tr>
<tr>
    <td align="center">undetermined</td>
    <td align="center">json_html_undetermined_sample</td>
</tr>
<tr>
    <td align="center">malicious_rate</td>
    <td align="center"><b>json_html_malicious_rate_sample</b></td>
</tr>
<tr>
    <td align="center" rowspan="5">java</td>
    <td align="center">total</td>
    <td align="center">json_java_total_sample</td>
</tr>
<tr>
    <td align="center">malicious</td>
    <td align="center">json_java_malicious_sample</td>
</tr>
<tr>
    <td align="center">monitoring</td>
    <td align="center">json_java_monitoring_sample</td>
</tr>
<tr>
    <td align="center">undetermined</td>
    <td align="center">json_java_undetermined_sample</td>
</tr>
<tr>
    <td align="center">malicious_rate</td>
    <td align="center"><b>json_java_malicious_rate_sample</b></td>
</tr>
<tr>
    <td align="center" rowspan="5">pdf</td>
    <td align="center">total</td>
    <td align="center">json_pdf_total_sample</td>
</tr>
<tr>
    <td align="center">malicious</td>
    <td align="center">json_pdf_malicious_sample</td>
</tr>
<tr>
    <td align="center">monitoring</td>
    <td align="center">json_pdf_monitoring_sample</td>
</tr>
<tr>
    <td align="center">undetermined</td>
    <td align="center">json_pdf_undetermined_sample</td>
</tr>
<tr>
    <td align="center">malicious_rate</td>
    <td align="center"><b>json_pdf_malicious_rate_sample</b></td>
</tr>
</tbody>
</table>
</div>
</body>
</html>
'''