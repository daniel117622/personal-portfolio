interface CalendarEvent {
  id?: string | number;
  name?: string;
  start: string;
  end: string;
  status: 'ACTIVE' | 'DECLINED' | 'CANCELED' | string;
}

interface Palette {
  bg: string;
  border: string;
  text: string;
}

// Directly extend the Window interface (no declare global needed in a non-module script)
interface Window {
  setEvents: (list: CalendarEvent[]) => void;
  addEvent: (ev: CalendarEvent) => void;
}

(function () {
  "use strict";

  function readEvents(): CalendarEvent[] {
    const node = document.getElementById("calEventsData");
    if (!node) return [];
    try {
      const parsed = JSON.parse(node.textContent || "[]");
      if (!Array.isArray(parsed)) return [];
      return parsed;
    } catch (err) {
      return [];
    }
  }

  const MONTH_NAMES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
  ];

  const DAY_NAMES = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"];

  const STATUS_COLORS: Record<string, Palette> = {
    ACTIVE:   { bg: '#f0fdf4', border: '#0f766e', text: '#115e59' },
    DECLINED: { bg: '#fff7ed', border: '#c2410c', text: '#9a3412' },
    CANCELED: { bg: '#f1f5f9', border: '#475569', text: '#334155' }
  };

  const START_HOUR = 8;
  const END_HOUR = 20;
  const MOBILE_DAYS = 5;
  const ROW_HEIGHT = 100;

  let events: CalendarEvent[] = readEvents();

  let eventsByDay: Record<string, CalendarEvent[]> = buildIndex(events);
  let cursor = initialCursor(events);

  const headEl = document.getElementById("calHead");
  const bodyEl = document.getElementById("calBody");
  const mobileEl = document.getElementById("calMobile");
  const labelEl = document.getElementById("calWeekLabel");
  const emptyEl = document.getElementById("calEmptyState");
  const prevBtn = document.getElementById("calPrevBtn");
  const nextBtn = document.getElementById("calNextBtn");

  if (!bodyEl || !headEl || !labelEl) return;

  if (prevBtn) {
    prevBtn.addEventListener("click", function () {
      cursor.setDate(cursor.getDate() - 7);
      render();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", function () {
      cursor.setDate(cursor.getDate() + 7);
      render();
    });
  }

  render();

  function getMonday(d: Date | string | number): Date {
    const nd = new Date(d);
    const day = nd.getDay();
    const diff = nd.getDate() - day + (day === 0 ? -6 : 1);
    nd.setDate(diff);
    nd.setHours(0, 0, 0, 0);
    return nd;
  }

  function dayKey(y: number, m: number, d: number): string {
    return y + "-" + m + "-" + d;
  }

  function sortEventsArray(arr: CalendarEvent[]) {
    arr.sort(function (a, b) {
      const timeA = new Date(a.start).getTime();
      const timeB = new Date(b.start).getTime();
      return timeA - timeB;
    });
  }

  function buildIndex(list: CalendarEvent[]): Record<string, CalendarEvent[]> {
    const idx: Record<string, CalendarEvent[]> = {};
    for (let i = 0; i < list.length; i++) {
      const ev = list[i];
      const start = new Date(ev.start);
      if (isNaN(start.getTime())) continue;

      const key = dayKey(start.getFullYear(), start.getMonth(), start.getDate());
      if (!idx[key]) idx[key] = [];
      idx[key].push(ev);
    }

    for (const k in idx) {
      sortEventsArray(idx[k]);
    }

    return idx;
  }

  function initialCursor(list: CalendarEvent[]): Date {
    if (!list.length) return getMonday(new Date());

    let earliest: Date | null = null;
    for (let i = 0; i < list.length; i++) {
      const d = new Date(list[i].start);
      if (isNaN(d.getTime())) continue;
      if (earliest === null || d < earliest) earliest = d;
    }
    if (earliest === null) return getMonday(new Date());
    return getMonday(earliest);
  }

  function hhmm(iso: string): string {
    const d = new Date(iso);
    if (isNaN(d.getTime())) return "--:--";
    const h = String(d.getHours()).padStart(2, "0");
    const m = String(d.getMinutes()).padStart(2, "0");
    return h + ":" + m;
  }

  function escapeHtml(str: string): string {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function formatWeekLabel(startDay: Date, endDay: Date): string {
    const m1 = MONTH_NAMES[startDay.getMonth()];
    const m2 = MONTH_NAMES[endDay.getMonth()];
    const y1 = startDay.getFullYear();
    const y2 = endDay.getFullYear();

    if (m1 === m2 && y1 === y2) {
      return startDay.getDate() + " - " + endDay.getDate() + " " + m1 + " " + y1;
    } else if (y1 === y2) {
      return startDay.getDate() + " " + m1.substring(0, 3) + " - " + endDay.getDate() + " " + m2.substring(0, 3) + " " + y1;
    } else {
      return startDay.getDate() + " " + m1.substring(0, 3) + " " + y1 + " - " + endDay.getDate() + " " + m2.substring(0, 3) + " " + y2;
    }
  }


  function eventPill(ev: CalendarEvent): string {
    const ACTIVE_PALETTES: Palette[] = [
      { bg: '#f0fdf4', border: '#0f766e', text: '#115e59' },
      { bg: '#f0f9ff', border: '#0284c7', text: '#0369a1' },
      { bg: '#faf5ff', border: '#9333ea', text: '#7e22ce' },
      { bg: '#fef3c7', border: '#d97706', text: '#b45309' }
    ];

    let c: Palette;
    if (ev.status === 'ACTIVE') {
      const str = String(ev.id || ev.name || '0');
      let hash = 5381;
      for (let i = 0; i < str.length; i++) {
        hash = ((hash * 33) ^ str.charCodeAt(i)) >>> 0;
      }
      c = ACTIVE_PALETTES[hash % ACTIVE_PALETTES.length];
    } else {
      c = STATUS_COLORS[ev.status] || STATUS_COLORS.CANCELED;
    }

    const label = hhmm(ev.start) + " - " + hhmm(ev.end) + " " + escapeHtml(ev.name || "Sin nombre");

    const s = new Date(ev.start);
    let e = new Date(ev.end);
    if (isNaN(s.getTime())) return '';
    if (isNaN(e.getTime()) || e <= s) {
      e = new Date(s.getTime() + 60 * 60000);
    }

    const startHourDec = s.getHours() + (s.getMinutes() / 60);
    const endHourDec = e.getHours() + (e.getMinutes() / 60);

    const visualStart = Math.max(START_HOUR, startHourDec);
    const visualEnd = Math.min(END_HOUR + 1, endHourDec);
    if (visualStart >= visualEnd) return '';

    const topPx = (visualStart - START_HOUR) * ROW_HEIGHT;
    const heightPx = (visualEnd - visualStart) * ROW_HEIGHT;

    return '<div style="' +
      'position: absolute; ' +
      'top: ' + topPx + 'px; ' +
      'left: 0; right: 0; ' +
      'height: ' + heightPx + 'px; ' +
      'box-sizing: border-box; ' +
      'background-color: ' + c.bg + '; ' +
      'border: none; ' +
      'border-left: 4px solid ' + c.border + '; ' +
      'color: ' + c.text + '; ' +
      'padding: 8px 10px; ' +
      'border-radius: 0; ' +
      'font-size: 0.78rem; ' +
      'font-weight: 600; ' +
      'overflow: hidden; ' +
      'z-index: 5; ' +
      'cursor: pointer;" title="' + escapeHtml(label) + '">' +
      '<div>' + hhmm(ev.start) + ' - ' + hhmm(ev.end) + '</div>' +
      '<div style="font-weight: 700; margin-top: 2px;">' + escapeHtml(ev.name || "Sin nombre") + '</div>' +
      '</div>';
  }

  function render() {
    const weekDays: Date[] = [];
    for (let i = 0; i < 7; i++) {
      const d = new Date(cursor);
      d.setDate(d.getDate() + i);
      weekDays.push(d);
    }

    if(labelEl) labelEl.textContent = formatWeekLabel(weekDays[0], weekDays[4]);

    let theadHtml = '<tr style="background-color: #f3f4f6; border-bottom: 1px solid #d1d5db;">';
    theadHtml += '<th style="width: 80px; padding: 12px 8px; border-right: 1px solid #d1d5db; color: #4b5563; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; text-align: center;">Hora</th>';

    for (let i = 0; i < 5; i++) {
      const isLast = (i === 4);
      const border = isLast ? '' : 'border-right: 1px solid #e5e7eb;';
      const dayName = DAY_NAMES[weekDays[i].getDay()];
      theadHtml += '<th style="padding: 12px 8px; ' + border + ' color: #111827; font-weight: 600; font-size: 0.85rem; text-align: center;">' +
        dayName + ' ' + weekDays[i].getDate() +
        '</th>';
    }
    theadHtml += '</tr>';
    if(headEl) headEl.innerHTML = theadHtml;

    let weekHasEvents = false;
    const totalHours = (END_HOUR - START_HOUR + 1);
    const totalHeight = totalHours * ROW_HEIGHT;

    let tbodyHtml = '<tr>';

    tbodyHtml += '<td style="padding: 0; border-right: 1px solid #d1d5db; width: 80px; vertical-align: top; background: #f9fafb;">';
    for (let h = START_HOUR; h <= END_HOUR; h++) {
      const hh = String(h).padStart(2, "0") + ":00";
      tbodyHtml += '<div style="height: ' + ROW_HEIGHT + 'px; box-sizing: border-box; border-bottom: 1px solid #e5e7eb; padding: 6px 4px; text-align: center; color: #6b7280; font-size: 0.82rem; font-weight: 500;">' + hh + '</div>';
    }
    tbodyHtml += '</td>';

    for (let d = 0; d < 5; d++) {
      const isLast = (d === 4);
      const border = isLast ? '' : 'border-right: 1px solid #e5e7eb;';
      const key = dayKey(weekDays[d].getFullYear(), weekDays[d].getMonth(), weekDays[d].getDate());
      const dayEvents = eventsByDay[key] || [];

      tbodyHtml += '<td style="padding: 0; ' + border + ' vertical-align: top; background-color: #ffffff; position: relative; height: ' + totalHeight + 'px;">';

      tbodyHtml += '<div style="position: absolute; inset: 0; pointer-events: none;">';
      for (let h = START_HOUR; h <= END_HOUR; h++) {
        tbodyHtml += '<div style="height: ' + ROW_HEIGHT + 'px; box-sizing: border-box; border-bottom: 1px solid #f3f4f6;"></div>';
      }
      tbodyHtml += '</div>';

      if (dayEvents.length > 0) {
        weekHasEvents = true;
        for (let e = 0; e < dayEvents.length; e++) {
          tbodyHtml += eventPill(dayEvents[e]);
        }
      }

      tbodyHtml += '</td>';
    }

    tbodyHtml += '</tr>';

    if(bodyEl) bodyEl.innerHTML = tbodyHtml;

    renderMobile(weekDays);

    if (emptyEl) {
      emptyEl.classList.toggle("d-none", weekHasEvents);
    }
  }

  function startOfDay(d: Date): Date {
    const c = new Date(d);
    c.setHours(0, 0, 0, 0);
    return c;
  }

  function sameDay(a: Date, b: Date): boolean {
    return startOfDay(a).getTime() === startOfDay(b).getTime();
  }

  function colorFor(ev: CalendarEvent): Palette {
    const ACTIVE_PALETTES: Palette[] = [
      { bg: '#f0fdf4', border: '#0f766e', text: '#115e59' },
      { bg: '#f0f9ff', border: '#0284c7', text: '#0369a1' },
      { bg: '#faf5ff', border: '#9333ea', text: '#7e22ce' },
      { bg: '#fef3c7', border: '#d97706', text: '#b45309' }
    ];
    if (ev.status !== 'ACTIVE') {
      return STATUS_COLORS[ev.status] || STATUS_COLORS.CANCELED;
    }
    const str = String(ev.id || ev.name || '0');
    let hash = 5381;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash * 33) ^ str.charCodeAt(i)) >>> 0;
    }
    return ACTIVE_PALETTES[hash % ACTIVE_PALETTES.length];
  }

  function mobileSlot(ev: CalendarEvent): string {
    const c = colorFor(ev);
    const time = hhmm(ev.start) + " - " + hhmm(ev.end);
    const name = escapeHtml(ev.name || "Sin nombre");
    return '<div style="padding: 10px 12px; border-bottom: 1px solid #f1f5f9; ' +
      'border-left: 4px solid ' + c.border + '; background-color: ' + c.bg + '; ' +
      'color: ' + c.text + ';">' +
      '<div style="font-size: 0.75rem; font-weight: 600;">' + time + '</div>' +
      '<div style="font-weight: 700; margin-top: 2px; font-size: 0.9rem;">' + name + '</div>' +
      '</div>';
  }

  function mobileDayCard(day: Date, isToday: boolean): string {
    const key = dayKey(day.getFullYear(), day.getMonth(), day.getDate());
    const items = eventsByDay[key] || [];
    const titleText = DAY_NAMES[day.getDay()] + " " + day.getDate() + (isToday ? " · Hoy" : "");

    const headerStyle = isToday
      ? 'background:#0f766e;color:#fff;'
      : 'background:#f3f4f6;color:#111827;';

    let html = '<div style="border:1px solid #d1d5db; border-radius:2px; ' +
      'margin-bottom:1rem; overflow:hidden;">';

    html += '<div class="d-flex justify-content-between align-items-baseline" ' +
      'style="' + headerStyle + 'padding:0.75rem 1rem; font-weight:600; ' +
      'border-bottom:1px solid #d1d5db;">' +
      '<span>' + titleText + '</span>' +
      '<span style="font-size:0.72rem; font-weight:500; opacity:0.85;">' +
      items.length + ' reserva(s)</span>' +
      '</div>';

    if (items.length === 0) {
      html += '<div class="text-center" style="padding:1rem; color:#9ca3af; ' +
        'font-size:0.85rem;">Sin reservaciones</div>';
    } else {
      for (let i = 0; i < items.length; i++) {
        html += mobileSlot(items[i]);
      }
    }

    html += '</div>';
    return html;
  }

  function renderMobile(weekDays: Date[]) {
    if (!mobileEl) return;

    const today = startOfDay(new Date());

    let startIdx = 0;
    for (let i = 0; i < weekDays.length; i++) {
      if (startOfDay(weekDays[i]).getTime() >= today.getTime()) {
        startIdx = i;
        break;
      }
    }

    let html = "";
    for (let n = 0; n < MOBILE_DAYS && startIdx + n < weekDays.length; n++) {
      const day = weekDays[startIdx + n];
      html += mobileDayCard(day, sameDay(day, today));
    }

    mobileEl.innerHTML = html;
  }

  window.setEvents = function (list: CalendarEvent[]) {
    events = list;
    eventsByDay = buildIndex(events);
    render();
  };

  window.addEvent = function (ev: CalendarEvent) {
    events.push(ev);

    const start = new Date(ev.start);
    if (!isNaN(start.getTime())) {
      const key = dayKey(start.getFullYear(), start.getMonth(), start.getDate());
      if (!eventsByDay[key]) eventsByDay[key] = [];

      eventsByDay[key].push(ev);
      sortEventsArray(eventsByDay[key]);
    }

    render();
  };

})();
