import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { FileDown, Loader } from 'lucide-react';
import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';
import axios from 'axios';

const ExportReportButton = ({ reportType = 'disease', customData = null }) => {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);

  const generatePDF = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      let data;

      // Fetch data based on report type
      if (customData) {
        data = customData;
      } else {
        const response = await axios.get(
          `http://localhost:8000/api/v1/reports/${reportType}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        data = response.data;
      }

      // Create PDF
      const doc = new jsPDF();
      const pageWidth = doc.internal.pageSize.width;
      const pageHeight = doc.internal.pageSize.height;

      // Header
      doc.setFillColor(34, 197, 94); // Primary green
      doc.rect(0, 0, pageWidth, 40, 'F');
      
      doc.setTextColor(255, 255, 255);
      doc.setFontSize(24);
      doc.text('AgriSmart AI', 15, 20);
      
      doc.setFontSize(12);
      doc.text(`${getReportTitle(reportType)}`, 15, 30);
      
      // Date
      doc.setFontSize(10);
      doc.text(`Generated: ${new Date().toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      })}`, pageWidth - 70, 30);

      // Reset text color
      doc.setTextColor(0, 0, 0);

      // Content based on report type
      let yPos = 50;

      if (reportType === 'disease') {
        yPos = generateDiseaseReport(doc, data, yPos);
      } else if (reportType === 'analytics') {
        yPos = generateAnalyticsReport(doc, data, yPos);
      } else if (reportType === 'farm-health') {
        yPos = generateHealthReport(doc, data, yPos);
      } else if (reportType === 'irrigation') {
        yPos = generateIrrigationReport(doc, data, yPos);
      }

      // Add page numbers and footer to all pages
      const totalPages = doc.internal.getNumberOfPages();
      
      for (let i = 1; i <= totalPages; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(128, 128, 128);
        doc.text('AgriSmart AI - Your Intelligent Agricultural Advisory Platform', pageWidth / 2, pageHeight - 10, { align: 'center' });
        doc.text(`Page ${i} of ${totalPages}`, pageWidth / 2, pageHeight - 5, { align: 'center' });
      }

      // Save PDF
      const fileName = `${reportType}-report-${new Date().toISOString().split('T')[0]}.pdf`;
      doc.save(fileName);

    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Failed to generate PDF report');
    } finally {
      setLoading(false);
    }
  };

  const getReportTitle = (type) => {
    const titles = {
      'disease': 'Disease Detection Report',
      'analytics': 'Disease Analytics Report',
      'farm-health': 'Farm Health Report',
      'irrigation': 'Irrigation Summary Report',
      'monthly': 'Monthly Farm Report'
    };
    return titles[type] || 'Farm Report';
  };

  const generateDiseaseReport = (doc, data, startY) => {
    let yPos = startY;

    // Summary Section
    doc.setFontSize(14);
    doc.setTextColor(34, 197, 94);
    doc.text('Summary', 15, yPos);
    yPos += 10;

    doc.setFontSize(10);
    doc.setTextColor(0, 0, 0);
    doc.text(`Total Detections: ${data.total_detections || 0}`, 20, yPos);
    yPos += 7;
    doc.text(`Healthy Scans: ${data.healthy_count || 0}`, 20, yPos);
    yPos += 7;
    doc.text(`Disease Detected: ${data.disease_count || 0}`, 20, yPos);
    yPos += 7;
    doc.text(`Health Rate: ${data.health_rate || 0}%`, 20, yPos);
    yPos += 15;

    // Detection History Table
    if (data.history && data.history.length > 0) {
      doc.setFontSize(14);
      doc.setTextColor(34, 197, 94);
      doc.text('Detection History', 15, yPos);
      yPos += 10;

      const tableData = data.history.slice(0, 10).map(d => [
        new Date(d.detected_at).toLocaleDateString(),
        d.crop_type || 'N/A',
        d.disease_detected,
        `${d.confidence}%`,
        d.severity
      ]);

      autoTable(doc, {
        startY: yPos,
        head: [['Date', 'Crop', 'Disease', 'Confidence', 'Severity']],
        body: tableData,
        theme: 'grid',
        headStyles: { fillColor: [34, 197, 94] },
        margin: { left: 15, right: 15 }
      });
    }

    return doc.lastAutoTable ? doc.lastAutoTable.finalY + 10 : yPos;
  };

  const generateHealthReport = (doc, data, startY) => {
    let yPos = startY;

    // Health Score
    doc.setFontSize(16);
    doc.setTextColor(34, 197, 94);
    doc.text('Farm Health Score', 15, yPos);
    yPos += 15;

    doc.setFontSize(40);
    const scoreColor = data.overall_score >= 80 ? [34, 197, 94] : 
                       data.overall_score >= 60 ? [234, 179, 8] : [239, 68, 68];
    doc.setTextColor(...scoreColor);
    doc.text(`${data.overall_score}`, 100, yPos, { align: 'center' });
    
    doc.setFontSize(12);
    doc.text('/ 100', 115, yPos);
    yPos += 15;

    // Metrics
    doc.setFontSize(10);
    doc.setTextColor(0, 0, 0);
    
    const metrics = [
      ['Health Rate', `${data.health_rate}%`],
      ['Total Scans', data.total_scans],
      ['Active Crops', data.active_crops],
      ['Issues Detected', data.issues_detected]
    ];

    autoTable(doc, {
      startY: yPos,
      body: metrics,
      theme: 'grid',
      columnStyles: {
        0: { fontStyle: 'bold', fillColor: [240, 240, 240] },
        1: { halign: 'right' }
      },
      margin: { left: 15, right: 100 }
    });

    yPos = doc.lastAutoTable.finalY + 15;

    // Recommendations
    if (data.recommendations && data.recommendations.length > 0) {
      doc.setFontSize(14);
      doc.setTextColor(34, 197, 94);
      doc.text('Recommendations', 15, yPos);
      yPos += 10;

      doc.setFontSize(10);
      doc.setTextColor(0, 0, 0);
      data.recommendations.forEach((rec, idx) => {
        // Remove emojis from recommendation text
        const cleanRec = rec.replace(/[\u{1F300}-\u{1F9FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]/gu, '').trim();
        doc.text(`${idx + 1}. ${cleanRec}`, 20, yPos);
        yPos += 7;
      });
    }

    return yPos;
  };

  const generateAnalyticsReport = (doc, data, startY) => {
    let yPos = startY;

    // Summary Statistics
    doc.setFontSize(14);
    doc.setTextColor(34, 197, 94);
    doc.text('Analytics Summary', 15, yPos);
    yPos += 10;

    doc.setFontSize(10);
    doc.setTextColor(0, 0, 0);
    doc.text(`Total Detections: ${data.trends?.total_detections || 0}`, 20, yPos);
    yPos += 7;
    doc.text(`Unique Diseases: ${data.trends?.unique_diseases || 0}`, 20, yPos);
    yPos += 7;
    doc.text(`Health Score: ${data.trends?.health_score || 0}`, 20, yPos);
    yPos += 7;
    doc.text(`Analysis Period: ${data.period_days || 30} days`, 20, yPos);
    yPos += 15;

    // Most Common Diseases
    if (data.trends?.most_common_diseases && data.trends.most_common_diseases.length > 0) {
      doc.setFontSize(14);
      doc.setTextColor(34, 197, 94);
      doc.text('Most Common Diseases', 15, yPos);
      yPos += 10;

      const diseaseData = data.trends.most_common_diseases.map(d => [
        d.disease,
        d.count,
        `${((d.count / (data.trends?.total_detections || 1)) * 100).toFixed(1)}%`
      ]);

      autoTable(doc, {
        startY: yPos,
        head: [['Disease Name', 'Count', 'Percentage']],
        body: diseaseData,
        theme: 'grid',
        headStyles: { fillColor: [34, 197, 94] },
        margin: { left: 15, right: 15 }
      });

      yPos = doc.lastAutoTable.finalY + 15;
    }

    // Severity Distribution
    if (data.trends?.severity_distribution && Object.keys(data.trends.severity_distribution).length > 0) {
      doc.setFontSize(14);
      doc.setTextColor(34, 197, 94);
      doc.text('Severity Distribution', 15, yPos);
      yPos += 10;

      const severityData = Object.entries(data.trends.severity_distribution).map(([severity, data]) => [
        severity || 'None',
        data.count || 0,
        `${data.percentage || 0}%`
      ]);

      autoTable(doc, {
        startY: yPos,
        head: [['Severity Level', 'Count', 'Percentage']],
        body: severityData,
        theme: 'grid',
        headStyles: { fillColor: [34, 197, 94] },
        margin: { left: 15, right: 15 }
      });

      yPos = doc.lastAutoTable.finalY + 15;
    }

    // Crop-wise Analysis
    if (data.trends?.crop_wise_diseases && Object.keys(data.trends.crop_wise_diseases).length > 0) {
      // Check if we need a new page
      const pageHeight = doc.internal.pageSize.height;
      if (yPos > pageHeight - 80) {
        doc.addPage();
        yPos = 20;
      }

      doc.setFontSize(14);
      doc.setTextColor(34, 197, 94);
      doc.text('Crop-wise Disease Analysis', 15, yPos);
      yPos += 10;

      Object.entries(data.trends.crop_wise_diseases).forEach(([crop, cropData]) => {
        doc.setFontSize(11);
        doc.setTextColor(0, 0, 0);
        doc.setFont(undefined, 'bold');
        doc.text(`${crop.charAt(0).toUpperCase() + crop.slice(1)}`, 20, yPos);
        doc.setFont(undefined, 'normal');
        yPos += 7;

        doc.setFontSize(9);
        doc.text(`Total Detections: ${cropData.total || 0}`, 25, yPos);
        yPos += 6;
        doc.text(`Unique Diseases: ${cropData.unique || 0}`, 25, yPos);
        yPos += 6;
        
        if (cropData.most_common && cropData.most_common.length > 0) {
          const mostCommonDisease = cropData.most_common[0][0];
          const mostCommonCount = cropData.most_common[0][1];
          doc.text(`Most Common: ${mostCommonDisease} (${mostCommonCount})`, 25, yPos);
          yPos += 10;
        } else {
          yPos += 4;
        }
      });

      yPos += 5;
    }

    // Detection History
    if (data.history && data.history.length > 0) {
      // Check if we need a new page
      const pageHeight = doc.internal.pageSize.height;
      if (yPos > pageHeight - 60) {
        doc.addPage();
        yPos = 20;
      }

      doc.setFontSize(14);
      doc.setTextColor(34, 197, 94);
      doc.text('Recent Detection History', 15, yPos);
      yPos += 10;

      const tableData = data.history.slice(0, 10).map(d => [
        new Date(d.created_at).toLocaleDateString(),
        d.crop_type || 'N/A',
        d.disease_name,
        `${d.confidence}%`,
        d.severity || 'N/A'
      ]);

      autoTable(doc, {
        startY: yPos,
        head: [['Date', 'Crop', 'Disease', 'Confidence', 'Severity']],
        body: tableData,
        theme: 'grid',
        headStyles: { fillColor: [34, 197, 94] },
        margin: { left: 15, right: 15 }
      });
    }

    return doc.lastAutoTable ? doc.lastAutoTable.finalY + 10 : yPos;
  };

  const generateIrrigationReport = (doc, data, startY) => {
    let yPos = startY;

    doc.setFontSize(14);
    doc.setTextColor(34, 197, 94);
    doc.text('Irrigation Summary', 15, yPos);
    yPos += 10;

    doc.setFontSize(10);
    doc.setTextColor(0, 0, 0);

    if (data.calculations) {
      doc.text(`Crop: ${data.crop_type || 'N/A'}`, 20, yPos);
      yPos += 7;
      doc.text(`Soil Type: ${data.soil_type || 'N/A'}`, 20, yPos);
      yPos += 7;
      doc.text(`Area: ${data.area_acres || 'N/A'} acres`, 20, yPos);
      yPos += 10;

      doc.text(`Daily Water Requirement: ${data.calculations.crop_water_requirement_mm_per_day || 0} mm/day`, 20, yPos);
      yPos += 7;
      doc.text(`Weekly Requirement: ${data.calculations.water_volume_liters || 0} L`, 20, yPos);
      yPos += 15;
    }

    // Schedule Table
    if (data.schedule && data.schedule.length > 0) {
      const tableData = data.schedule.map(s => [
        `Day ${s.day}`,
        `${s.water_liters} L`,
        s.morning_recommended ? '6-8 AM' : 'Evening'
      ]);

      autoTable(doc, {
        startY: yPos,
        head: [['Day', 'Water Amount', 'Best Time']],
        body: tableData,
        theme: 'grid',
        headStyles: { fillColor: [34, 197, 94] },
        margin: { left: 15, right: 15 }
      });
    }

    return yPos;
  };

  return (
    <button
      onClick={generatePDF}
      disabled={loading}
      className="btn-secondary flex items-center gap-2"
      title="Export to PDF"
    >
      {loading ? (
        <>
          <Loader className="w-4 h-4 animate-spin" />
          {t('generating')}
        </>
      ) : (
        <>
          <FileDown className="w-4 h-4" />
          {t('export_pdf')}
        </>
      )}
    </button>
  );
};

export default ExportReportButton;
