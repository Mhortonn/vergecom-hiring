import { useState, useEffect, useRef } from "react";

const SKILLS = [
  "Satellite systems (DirecTV, HughesNet)",
  "Starlink installation",
  "TV mounting",
  "Security camera installation",
  "Low voltage wiring (Cat5/Coax)",
  "Smart home systems",
  "No installation experience",
];
const TOOLS = ["Power drill", "Crimper tools", "Cable tester", "Fish tape", "Stud finder", "Signal meter"];
const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
const YEARS_OPTIONS = ["Less than 1 year", "1-2 years", "3-5 years", "5-10 years", "10+ years"];
const RADIUS_OPTIONS = ["15 miles", "30 miles", "50 miles", "75 miles", "100+ miles"];

// ─── Reusable UI Components ─────────────────────────────────────────────────

function TextInput({ label, required, value, onChange, placeholder, half }) {
  return (
    <div style={{ flex: half ? "1 1 48%" : "1 1 100%", minWidth: half ? 200 : "auto" }}>
      <label style={styles.label}>
        {label} {required && <span style={styles.req}>*</span>}
      </label>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder || ""}
        style={styles.input}
        onFocus={(e) => (e.target.style.borderColor = "#0066FF")}
        onBlur={(e) => (e.target.style.borderColor = "#E2E4E9")}
      />
    </div>
  );
}

function SelectInput({ label, required, value, onChange, options }) {
  return (
    <div style={{ flex: "1 1 48%", minWidth: 200 }}>
      <label style={styles.label}>
        {label} {required && <span style={styles.req}>*</span>}
      </label>
      <select value={value} onChange={(e) => onChange(e.target.value)} style={styles.select}>
        <option value="">Select...</option>
        {options.map((o) => (
          <option key={o} value={o}>{o}</option>
        ))}
      </select>
    </div>
  );
}

function RadioGroup({ label, required, options, value, onChange }) {
  return (
    <div style={{ flex: "1 1 48%", minWidth: 200 }}>
      <label style={styles.label}>
        {label} {required && <span style={styles.req}>*</span>}
      </label>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 4 }}>
        {options.map((o) => (
          <button
            type="button"
            key={o}
            onClick={() => onChange(o)}
            style={{
              ...styles.radioBtn,
              background: value === o ? "#0066FF" : "#F7F8FA",
              color: value === o ? "#fff" : "#4A4F5C",
              borderColor: value === o ? "#0066FF" : "#E2E4E9",
            }}
          >
            {o}
          </button>
        ))}
      </div>
    </div>
  );
}

function ChipSelect({ label, required, options, selected, onToggle }) {
  return (
    <div>
      <label style={styles.label}>
        {label} {required && <span style={styles.req}>*</span>}
      </label>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 4 }}>
        {options.map((o) => {
          const active = selected.includes(o);
          return (
            <button
              type="button"
              key={o}
              onClick={() => onToggle(o)}
              style={{
                ...styles.chip,
                background: active ? "#EBF2FF" : "#F7F8FA",
                color: active ? "#0052CC" : "#4A4F5C",
                borderColor: active ? "#0066FF" : "#E2E4E9",
                fontWeight: active ? 600 : 400,
              }}
            >
              {active && <span style={{ marginRight: 4 }}>✓</span>}
              {o}
            </button>
          );
        })}
      </div>
    </div>
  );
}

function CheckItem({ label, checked, onChange }) {
  return (
    <label
      style={{
        display: "flex",
        alignItems: "center",
        gap: 8,
        cursor: "pointer",
        padding: "6px 0",
        fontSize: 14,
        color: "#3A3F4B",
        fontFamily: "'DM Sans', sans-serif",
      }}
    >
      <span
        style={{
          width: 18,
          height: 18,
          borderRadius: 4,
          border: checked ? "none" : "2px solid #CDD0D7",
          background: checked ? "#0066FF" : "#fff",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexShrink: 0,
          transition: "all .15s",
        }}
      >
        {checked && (
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M2.5 6L5 8.5L9.5 3.5" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        )}
      </span>
      {label}
    </label>
  );
}

function SectionCard({ number, title, icon, children, isActive, isComplete }) {
  return (
    <div
      style={{
        ...styles.section,
        borderColor: isActive ? "#0066FF" : isComplete ? "#00B37E" : "#ECEEF2",
        opacity: 1,
      }}
    >
      <div style={styles.sectionHeader}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div
            style={{
              ...styles.sectionNumber,
              background: isComplete ? "#00B37E" : isActive ? "#0066FF" : "#E8EAF0",
              color: isComplete || isActive ? "#fff" : "#7A7F8D",
            }}
          >
            {isComplete ? (
              <svg width="14" height="14" viewBox="0 0 12 12" fill="none">
                <path d="M2.5 6L5 8.5L9.5 3.5" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            ) : (
              number
            )}
          </div>
          <div>
            <div style={styles.sectionTitle}>{title}</div>
          </div>
        </div>
        <span style={{ fontSize: 20 }}>{icon}</span>
      </div>
      <div style={{ padding: "0 24px 24px" }}>{children}</div>
    </div>
  );
}

function ProgressBar({ step, total }) {
  const pct = Math.round((step / total) * 100);
  return (
    <div style={{ marginBottom: 32 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
        <span style={{ fontSize: 13, color: "#7A7F8D", fontFamily: "'DM Sans', sans-serif" }}>
          Application progress
        </span>
        <span style={{ fontSize: 13, fontWeight: 600, color: "#0066FF", fontFamily: "'DM Sans', sans-serif" }}>
          {pct}%
        </span>
      </div>
      <div style={{ height: 6, background: "#ECEEF2", borderRadius: 3, overflow: "hidden" }}>
        <div
          style={{
            height: "100%",
            width: `${pct}%`,
            background: "linear-gradient(90deg, #0066FF, #00B3FF)",
            borderRadius: 3,
            transition: "width .4s ease",
          }}
        />
      </div>
    </div>
  );
}

// ─── Main Application ───────────────────────────────────────────────────────

export default function StarlinkApplication() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setMounted(true), 100);
    return () => clearTimeout(t);
  }, []);

  // Form state
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [street, setStreet] = useState("");
  const [city, setCity] = useState("");
  const [st, setSt] = useState("");
  const [zip, setZip] = useState("");
  const [skills, setSkills] = useState([]);
  const [years, setYears] = useState("");
  const [roofWork, setRoofWork] = useState("");
  const [taskDrill, setTaskDrill] = useState(false);
  const [taskAttic, setTaskAttic] = useState(false);
  const [taskHeight, setTaskHeight] = useState(false);
  const [taskNet, setTaskNet] = useState(false);
  const [vehicle, setVehicle] = useState("");
  const [licenseValid, setLicenseValid] = useState("");
  const [ladder, setLadder] = useState("");
  const [tools, setTools] = useState([]);
  const [insurance, setInsurance] = useState("");
  const [startDate, setStartDate] = useState("");
  const [daysAvail, setDaysAvail] = useState([]);
  const [counties, setCounties] = useState("");
  const [radius, setRadius] = useState("30 miles");
  const [submitted, setSubmitted] = useState(false);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");

  const toggleList = (list, setList, item) => {
    setList((prev) => (prev.includes(item) ? prev.filter((x) => x !== item) : [...prev, item]));
  };

  // Progress calculation
  const sectionsDone = [
    name && phone && email,
    skills.length > 0 && years,
    vehicle && licenseValid,
    !!insurance,
    !!startDate && daysAvail.length > 0,
    !!counties,
  ];
  const completedSections = sectionsDone.filter(Boolean).length;

  const handleSubmit = () => {
    if (!name || !phone || !email || !counties) {
      setError("Please fill in all required fields marked with *");
      return;
    }
    setError("");

    let appStatus = "QUALIFIED";
    let isRejected = false;
    if (skills.includes("No installation experience")) isRejected = true;
    if (vehicle === "No") isRejected = true;
    if (licenseValid === "No") isRejected = true;
    if (insurance === "No") isRejected = true;

    if (isRejected) {
      appStatus = "REJECTED";
    } else {
      const hasSatExp = skills.some((s) =>
        ["Satellite systems (DirecTV, HughesNet)", "Starlink installation"].includes(s)
      );
      const hasIns = insurance === "Yes, I currently have insurance";
      if (hasSatExp && hasIns && ["Yes - Truck", "Yes - Van"].includes(vehicle)) {
        appStatus = "PRIORITY";
      }
    }

    setStatus(appStatus);
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div style={styles.page}>
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />
        <div style={{ ...styles.container, textAlign: "center", padding: "80px 40px" }}>
          <div style={styles.logoBar}>
            <div style={styles.logo}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0066FF" strokeWidth="2.5"><circle cx="12" cy="12" r="3"/><path d="M12 1v4m0 14v4M4.22 4.22l2.83 2.83m9.9 9.9l2.83 2.83M1 12h4m14 0h4M4.22 19.78l2.83-2.83m9.9-9.9l2.83-2.83"/></svg>
              <span style={styles.logoText}>STARLINK</span>
              <span style={{ ...styles.logoText, fontWeight: 400, color: "#7A7F8D" }}>TECH</span>
            </div>
          </div>
          {status === "REJECTED" ? (
            <>
              <div style={{ width: 64, height: 64, borderRadius: "50%", background: "#FFF1F0", display: "inline-flex", alignItems: "center", justifyContent: "center", marginBottom: 24 }}>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#E5484D" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M15 9l-6 6M9 9l6 6"/></svg>
              </div>
              <h2 style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 24, color: "#1A1D23", margin: "0 0 12px" }}>Application Not Accepted</h2>
              <p style={{ fontFamily: "'DM Sans', sans-serif", color: "#7A7F8D", maxWidth: 460, margin: "0 auto", lineHeight: 1.6 }}>
                Thank you for your interest. Based on our current requirements, we're unable to proceed with your application at this time. We encourage you to reapply once you meet the minimum qualifications.
              </p>
            </>
          ) : (
            <>
              <div style={{ width: 64, height: 64, borderRadius: "50%", background: "#ECFDF3", display: "inline-flex", alignItems: "center", justifyContent: "center", marginBottom: 24 }}>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#00B37E" strokeWidth="2.5"><path d="M20 6L9 17l-5-5"/></svg>
              </div>
              <h2 style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 24, color: "#1A1D23", margin: "0 0 12px" }}>Application Received</h2>
              {status === "PRIORITY" && (
                <div style={{ display: "inline-flex", alignItems: "center", gap: 6, padding: "4px 14px", borderRadius: 20, background: "#FFF7ED", border: "1px solid #FBBF24", marginBottom: 16, fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 600, color: "#B45309" }}>
                  ★ Priority Candidate
                </div>
              )}
              <p style={{ fontFamily: "'DM Sans', sans-serif", color: "#7A7F8D", maxWidth: 460, margin: "0 auto 8px", lineHeight: 1.6 }}>
                Thank you, <strong style={{ color: "#1A1D23" }}>{name}</strong>. Your qualifications are a strong match.
              </p>
              <p style={{ fontFamily: "'DM Sans', sans-serif", color: "#7A7F8D", maxWidth: 460, margin: "0 auto", lineHeight: 1.6 }}>
                Our hiring team will review your file and contact you at <strong style={{ color: "#1A1D23" }}>{phone}</strong> within 24 hours.
              </p>
            </>
          )}
        </div>
      </div>
    );
  }

  return (
    <div style={styles.page}>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />

      {/* Top bar */}
      <div style={styles.topBar}>
        <div style={styles.topBarInner}>
          <div style={styles.logo}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0066FF" strokeWidth="2.5"><circle cx="12" cy="12" r="3"/><path d="M12 1v4m0 14v4M4.22 4.22l2.83 2.83m9.9 9.9l2.83 2.83M1 12h4m14 0h4M4.22 19.78l2.83-2.83m9.9-9.9l2.83-2.83"/></svg>
            <span style={styles.logoText}>STARLINK</span>
            <span style={{ ...styles.logoText, fontWeight: 400, color: "#7A7F8D" }}>TECH</span>
          </div>
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: "#7A7F8D" }}>
            Field Technician Application
          </div>
        </div>
      </div>

      {/* Hero */}
      <div
        style={{
          ...styles.hero,
          opacity: mounted ? 1 : 0,
          transform: mounted ? "translateY(0)" : "translateY(12px)",
          transition: "all .6s ease",
        }}
      >
        <div style={styles.heroBadge}>NOW HIRING</div>
        <h1 style={styles.heroTitle}>Starlink Installation Technician</h1>
        <p style={styles.heroSub}>
          Apply to become a Certified Field Technician — Independent Contractor (1099)
        </p>
        <div style={styles.heroStats}>
          <div style={styles.heroStat}>
            <div style={styles.heroStatValue}>$45-75</div>
            <div style={styles.heroStatLabel}>Per Install</div>
          </div>
          <div style={styles.heroDivider} />
          <div style={styles.heroStat}>
            <div style={styles.heroStatValue}>Flexible</div>
            <div style={styles.heroStatLabel}>Schedule</div>
          </div>
          <div style={styles.heroDivider} />
          <div style={styles.heroStat}>
            <div style={styles.heroStatValue}>Training</div>
            <div style={styles.heroStatLabel}>Provided</div>
          </div>
        </div>
      </div>

      {/* Form */}
      <div style={styles.container}>
        <ProgressBar step={completedSections} total={6} />

        {/* 1. Contact */}
        <SectionCard number={1} title="Contact Information" icon="👤" isActive={!sectionsDone[0]} isComplete={!!sectionsDone[0]}>
          <div style={styles.fieldRow}>
            <TextInput label="Full Name" required value={name} onChange={setName} />
          </div>
          <div style={styles.fieldRow}>
            <TextInput label="Phone Number" required value={phone} onChange={setPhone} half />
            <TextInput label="Email Address" required value={email} onChange={setEmail} half />
          </div>
          <div style={{ ...styles.fieldRow, marginTop: 8 }}>
            <TextInput label="Street Address" value={street} onChange={setStreet} />
          </div>
          <div style={styles.fieldRow}>
            <TextInput label="City" value={city} onChange={setCity} half />
            <TextInput label="State" value={st} onChange={setSt} half />
          </div>
          <div style={{ ...styles.fieldRow, maxWidth: 200 }}>
            <TextInput label="ZIP Code" value={zip} onChange={setZip} />
          </div>
        </SectionCard>

        {/* 2. Experience */}
        <SectionCard number={2} title="Experience & Qualifications" icon="🛠" isActive={sectionsDone[0] && !sectionsDone[1]} isComplete={!!sectionsDone[1]}>
          <ChipSelect label="Installation experience" required options={SKILLS} selected={skills} onToggle={(s) => toggleList(skills, setSkills, s)} />
          <div style={{ ...styles.fieldRow, marginTop: 16 }}>
            <SelectInput label="Years of Experience" required value={years} onChange={setYears} options={YEARS_OPTIONS} />
            <RadioGroup label="Roof experience" required value={roofWork} onChange={setRoofWork} options={["Yes, comfortable", "Yes, limited", "No, but willing", "No"]} />
          </div>
          <div style={{ marginTop: 16 }}>
            <label style={styles.label}>Comfortable with these tasks</label>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0 24px", marginTop: 4 }}>
              <CheckItem label="Drilling through walls/roofs" checked={taskDrill} onChange={() => setTaskDrill(!taskDrill)} />
              <CheckItem label="Running cables in attics" checked={taskAttic} onChange={() => setTaskAttic(!taskAttic)} />
              <CheckItem label="Working at heights (20ft+)" checked={taskHeight} onChange={() => setTaskHeight(!taskHeight)} />
              <CheckItem label="Troubleshooting network issues" checked={taskNet} onChange={() => setTaskNet(!taskNet)} />
            </div>
          </div>
        </SectionCard>

        {/* 3. Vehicle & Equipment */}
        <SectionCard number={3} title="Vehicle & Equipment" icon="🚗" isActive={sectionsDone[1] && !sectionsDone[2]} isComplete={!!sectionsDone[2]}>
          <RadioGroup label="Reliable vehicle" required value={vehicle} onChange={setVehicle} options={["Yes - Truck", "Yes - Van", "Yes - SUV", "No"]} />
          <div style={{ ...styles.fieldRow, marginTop: 16 }}>
            <RadioGroup label="Valid Driver's License" required value={licenseValid} onChange={setLicenseValid} options={["Yes", "No"]} />
            <RadioGroup label="28ft+ extension ladder" required value={ladder} onChange={setLadder} options={["Yes, I own one", "No, but I can get one", "No"]} />
          </div>
          <div style={{ marginTop: 16 }}>
            <ChipSelect label="Tools owned" options={TOOLS} selected={tools} onToggle={(t) => toggleList(tools, setTools, t)} />
          </div>
        </SectionCard>

        {/* 4. Insurance */}
        <SectionCard number={4} title="Insurance" icon="🛡" isActive={sectionsDone[2] && !sectionsDone[3]} isComplete={!!sectionsDone[3]}>
          <RadioGroup
            label="General Liability Insurance"
            required
            value={insurance}
            onChange={setInsurance}
            options={["Yes, I currently have insurance", "No, but I can obtain within 1 week", "No, but I can obtain within 2 weeks", "No"]}
          />
        </SectionCard>

        {/* 5. Availability */}
        <SectionCard number={5} title="Availability" icon="📅" isActive={sectionsDone[3] && !sectionsDone[4]} isComplete={!!sectionsDone[4]}>
          <div style={styles.fieldRow}>
            <SelectInput label="When can you start?" value={startDate} onChange={setStartDate} options={["Immediately", "Within 1 week", "Within 2 weeks"]} />
            <div style={{ flex: "1 1 48%", minWidth: 200 }}>
              <label style={styles.label}>Employment Type</label>
              <div style={{ ...styles.input, display: "flex", alignItems: "center", background: "#F7F8FA", color: "#4A4F5C", cursor: "default", fontFamily: "'DM Sans', sans-serif", fontSize: 14 }}>
                Independent Contractor (1099)
              </div>
            </div>
          </div>
          <div style={{ marginTop: 12 }}>
            <ChipSelect label="Days available" options={DAYS} selected={daysAvail} onToggle={(d) => toggleList(daysAvail, setDaysAvail, d)} />
          </div>
        </SectionCard>

        {/* 6. Service Area */}
        <SectionCard number={6} title="Service Area" icon="📍" isActive={sectionsDone[4] && !sectionsDone[5]} isComplete={!!sectionsDone[5]}>
          <div>
            <label style={styles.label}>
              Counties you're willing to work in <span style={styles.req}>*</span>
            </label>
            <textarea
              value={counties}
              onChange={(e) => setCounties(e.target.value)}
              placeholder="e.g. Orange County, Lake County, Seminole County"
              rows={3}
              style={{ ...styles.input, resize: "vertical", minHeight: 72, fontFamily: "'DM Sans', sans-serif" }}
              onFocus={(e) => (e.target.style.borderColor = "#0066FF")}
              onBlur={(e) => (e.target.style.borderColor = "#E2E4E9")}
            />
          </div>
          <div style={{ marginTop: 16 }}>
            <label style={styles.label}>Max travel radius</label>
            <div style={{ display: "flex", gap: 8, marginTop: 4 }}>
              {RADIUS_OPTIONS.map((r) => (
                <button
                  type="button"
                  key={r}
                  onClick={() => setRadius(r)}
                  style={{
                    ...styles.radioBtn,
                    flex: 1,
                    background: radius === r ? "#0066FF" : "#F7F8FA",
                    color: radius === r ? "#fff" : "#4A4F5C",
                    borderColor: radius === r ? "#0066FF" : "#E2E4E9",
                  }}
                >
                  {r}
                </button>
              ))}
            </div>
          </div>
        </SectionCard>

        {/* Error */}
        {error && (
          <div style={styles.errorBanner}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#E5484D" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/></svg>
            {error}
          </div>
        )}

        {/* Submit */}
        <button type="button" onClick={handleSubmit} style={styles.submitBtn} onMouseEnter={(e) => { e.target.style.background = "#0052CC"; e.target.style.transform = "translateY(-1px)"; }} onMouseLeave={(e) => { e.target.style.background = "#0066FF"; e.target.style.transform = "translateY(0)"; }}>
          Submit Application
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M5 12h14m-6-6l6 6-6 6"/></svg>
        </button>

        <p style={styles.footer}>
          By submitting this application, you agree to our terms and conditions. All information is kept confidential.
        </p>
      </div>
    </div>
  );
}

// ─── Styles ─────────────────────────────────────────────────────────────────

const styles = {
  page: {
    minHeight: "100vh",
    background: "#F4F5F7",
    fontFamily: "'DM Sans', sans-serif",
  },
  topBar: {
    position: "sticky",
    top: 0,
    zIndex: 100,
    background: "rgba(255,255,255,.92)",
    backdropFilter: "blur(12px)",
    borderBottom: "1px solid #ECEEF2",
  },
  topBarInner: {
    maxWidth: 720,
    margin: "0 auto",
    padding: "12px 24px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  logo: {
    display: "flex",
    alignItems: "center",
    gap: 8,
  },
  logoText: {
    fontFamily: "'Space Grotesk', sans-serif",
    fontWeight: 700,
    fontSize: 15,
    letterSpacing: "0.04em",
    color: "#1A1D23",
  },
  logoBar: {
    display: "flex",
    justifyContent: "center",
    marginBottom: 32,
  },
  hero: {
    maxWidth: 720,
    margin: "0 auto",
    padding: "48px 24px 40px",
    textAlign: "center",
  },
  heroBadge: {
    display: "inline-block",
    fontFamily: "'DM Sans', sans-serif",
    fontSize: 11,
    fontWeight: 700,
    letterSpacing: "0.08em",
    color: "#00875A",
    background: "#E3FBF0",
    padding: "4px 14px",
    borderRadius: 20,
    marginBottom: 16,
  },
  heroTitle: {
    fontFamily: "'Space Grotesk', sans-serif",
    fontSize: 32,
    fontWeight: 700,
    color: "#1A1D23",
    margin: "0 0 10px",
    lineHeight: 1.2,
  },
  heroSub: {
    fontFamily: "'DM Sans', sans-serif",
    fontSize: 15,
    color: "#7A7F8D",
    margin: "0 0 28px",
  },
  heroStats: {
    display: "inline-flex",
    alignItems: "center",
    gap: 24,
    background: "#fff",
    borderRadius: 14,
    padding: "16px 32px",
    boxShadow: "0 1px 3px rgba(0,0,0,.06)",
    border: "1px solid #ECEEF2",
  },
  heroStat: { textAlign: "center" },
  heroStatValue: {
    fontFamily: "'Space Grotesk', sans-serif",
    fontSize: 18,
    fontWeight: 700,
    color: "#1A1D23",
  },
  heroStatLabel: {
    fontFamily: "'DM Sans', sans-serif",
    fontSize: 12,
    color: "#9CA1AE",
    marginTop: 2,
  },
  heroDivider: {
    width: 1,
    height: 32,
    background: "#ECEEF2",
  },
  container: {
    maxWidth: 720,
    margin: "0 auto",
    padding: "0 24px 64px",
  },
  section: {
    background: "#fff",
    borderRadius: 14,
    border: "2px solid #ECEEF2",
    marginBottom: 16,
    transition: "border-color .3s ease",
  },
  sectionHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "20px 24px 16px",
  },
  sectionNumber: {
    width: 28,
    height: 28,
    borderRadius: 8,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 13,
    fontWeight: 700,
    fontFamily: "'Space Grotesk', sans-serif",
    transition: "all .3s ease",
  },
  sectionTitle: {
    fontFamily: "'Space Grotesk', sans-serif",
    fontSize: 16,
    fontWeight: 600,
    color: "#1A1D23",
  },
  label: {
    display: "block",
    fontFamily: "'DM Sans', sans-serif",
    fontSize: 13,
    fontWeight: 600,
    color: "#4A4F5C",
    marginBottom: 6,
  },
  req: { color: "#E5484D" },
  input: {
    width: "100%",
    padding: "10px 14px",
    border: "1.5px solid #E2E4E9",
    borderRadius: 10,
    fontSize: 14,
    fontFamily: "'DM Sans', sans-serif",
    color: "#1A1D23",
    background: "#fff",
    outline: "none",
    transition: "border-color .2s",
    boxSizing: "border-box",
  },
  select: {
    width: "100%",
    padding: "10px 14px",
    border: "1.5px solid #E2E4E9",
    borderRadius: 10,
    fontSize: 14,
    fontFamily: "'DM Sans', sans-serif",
    color: "#1A1D23",
    background: "#fff",
    outline: "none",
    cursor: "pointer",
    boxSizing: "border-box",
  },
  fieldRow: {
    display: "flex",
    flexWrap: "wrap",
    gap: 16,
    marginBottom: 8,
  },
  radioBtn: {
    padding: "8px 16px",
    borderRadius: 8,
    border: "1.5px solid #E2E4E9",
    fontSize: 13,
    fontFamily: "'DM Sans', sans-serif",
    cursor: "pointer",
    transition: "all .15s",
    outline: "none",
    whiteSpace: "nowrap",
  },
  chip: {
    padding: "7px 14px",
    borderRadius: 20,
    border: "1.5px solid #E2E4E9",
    fontSize: 13,
    fontFamily: "'DM Sans', sans-serif",
    cursor: "pointer",
    transition: "all .15s",
    outline: "none",
  },
  errorBanner: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "12px 18px",
    background: "#FFF1F0",
    border: "1px solid #FDD8D8",
    borderRadius: 10,
    fontSize: 14,
    color: "#C4280D",
    fontFamily: "'DM Sans', sans-serif",
    marginBottom: 16,
  },
  submitBtn: {
    width: "100%",
    padding: "14px 24px",
    background: "#0066FF",
    color: "#fff",
    border: "none",
    borderRadius: 12,
    fontSize: 16,
    fontWeight: 600,
    fontFamily: "'DM Sans', sans-serif",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    transition: "all .2s ease",
    boxShadow: "0 2px 8px rgba(0,102,255,.25)",
  },
  footer: {
    textAlign: "center",
    fontSize: 12,
    color: "#9CA1AE",
    marginTop: 16,
    fontFamily: "'DM Sans', sans-serif",
  },
};
