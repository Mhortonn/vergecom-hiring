<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vergecom · Starlink technician</title>
    <!-- Font & base styling (identical to original premium look) -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: radial-gradient(circle at top right, #111827, #05070A);
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #94A3B8;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem 1rem;
        }

        .glass-panel {
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 32px;
            padding: 3rem 2.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        .company-tag {
            color: #3B82F6;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.2em;
            font-size: 0.8rem;
            margin-bottom: 1rem;
            display: block;
        }

        h1 {
            color: #FFFFFF;
            font-size: 3.2rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.1;
            margin-bottom: 1rem;
        }

        .subhead {
            color: #64748B;
            font-size: 1.25rem;
            font-weight: 400;
            margin-bottom: 2rem;
        }

        .info-grid {
            display: flex;
            gap: 1.5rem;
            margin: 2.5rem 0 2rem;
        }

        .info-tile {
            flex: 1;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 1.5rem 1.2rem;
            transition: 0.2s ease;
        }

        .info-tile:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(59, 130, 246, 0.3);
        }

        .info-label {
            color: #64748B;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.6rem;
        }

        .info-value {
            color: #FFFFFF;
            font-size: 1.3rem;
            font-weight: 700;
            line-height: 1.3;
        }

        .section-title {
            color: #FFFFFF;
            font-size: 0.75rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin: 2.5rem 0 1.2rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .desc-text {
            font-size: 1.1rem;
            line-height: 1.6;
            color: #94A3B8;
            margin-bottom: 1.8rem;
        }

        .two-col {
            display: flex;
            gap: 2rem;
            margin-bottom: 2rem;
        }

        .col {
            flex: 1;
        }

        .requirement-list {
            list-style: none;
        }

        .requirement-list li {
            display: flex;
            align-items: flex-start;
            margin-bottom: 0.8rem;
            color: #94A3B8;
            font-size: 0.95rem;
        }

        .requirement-list li::before {
            content: "→";
            color: #3B82F6;
            margin-right: 0.75rem;
            font-weight: 800;
        }

        .btn-primary {
            background: #3B82F6;
            color: white;
            border: none;
            border-radius: 14px;
            padding: 1rem 2rem;
            font-weight: 700;
            font-size: 1.1rem;
            width: 100%;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3);
            font-family: 'Plus Jakarta Sans', sans-serif;
            margin-top: 2rem;
        }

        .btn-primary:hover {
            background: #2563EB;
            transform: translateY(-2px);
            box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.4);
        }

        .btn-outline {
            background: transparent;
            color: #94A3B8;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: 0.2s;
            margin-bottom: 1.5rem;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }

        .btn-outline:hover {
            border-color: #3B82F6;
            color: white;
        }

        .form-group {
            margin-bottom: 1.6rem;
        }

        label {
            color: #FFFFFF;
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 0.4rem;
            display: block;
        }

        input, select, .multifake {
            width: 100%;
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            padding: 0.85rem 1.2rem;
            color: #FFFFFF;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.95rem;
            transition: 0.2s;
        }

        input:focus, select:focus {
            outline: none;
            border-color: #3B82F6;
            background: rgba(0, 0, 0, 0.4);
        }

        .radio-group {
            display: flex;
            gap: 1.5rem;
            background: rgba(0, 0, 0, 0.2);
            padding: 0.8rem 1.2rem;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .radio-option {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            color: #CBD5E1;
        }

        .chip {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 30px;
            padding: 0.3rem 1rem;
            font-size: 0.9rem;
            color: #CBD5E1;
            margin-right: 0.5rem;
            display: inline-block;
        }

        .success-icon {
            font-size: 3.5rem;
            margin-bottom: 1rem;
        }

        .text-center { text-align: center; }

        /* hide default number spinners, etc */
        input[type=number]::-webkit-inner-spin-button { opacity: 0; }
        hr { border: 0.5px solid rgba(255,255,255,0.05); margin: 2rem 0; }

        /* for demonstration we use a subtle transition between pages */
        .page {
            display: block;
        }
    </style>
</head>
<body>
    <!-- main container simulates streamlit multi-page with hidden inputs & js -->
    <div class="glass-panel" id="appRoot">
        <!-- page 1: landing (visible by default) -->
        <div id="landingPage" class="page">
            <span class="company-tag">Vergecom LLC</span>
            <h1>Starlink<br>Technician</h1>
            <p class="subhead">Join our elite field force as an Independent Contractor (1099).</p>
            
            <div class="info-grid">
                <div class="info-tile">
                    <div class="info-label">Compensation</div>
                    <div class="info-value">$1,200 – $1,800 / wk</div>
                </div>
                <div class="info-tile">
                    <div class="info-label">Location</div>
                    <div class="info-value">Greater Metro Area</div>
                </div>
            </div>

            <div class="section-title">Position Summary</div>
            <p class="desc-text">Vergecom is seeking professional Field Technicians to install and service Starlink satellite systems. This is a high‑volume, performance‑driven role for those with technical precision.</p>

            <div class="two-col">
                <div class="col">
                    <div class="section-title">Responsibilities</div>
                    <ul class="requirement-list">
                        <li>3‑6 precision installs daily</li>
                        <li>Advanced roof mounting</li>
                        <li>Cable termination & alignment</li>
                    </ul>
                </div>
                <div class="col">
                    <div class="section-title">Requirements</div>
                    <ul class="requirement-list">
                        <li>Truck / Van / SUV</li>
                        <li>28ft Fiberglass ladder</li>
                        <li>Liability insurance</li>
                    </ul>
                </div>
            </div>

            <button class="btn-primary" id="beginBtn">Begin Application →</button>
        </div>

        <!-- page 2: application (hidden initially) -->
        <div id="applicationPage" class="page" style="display: none;">
            <button class="btn-outline" id="backToLandingBtn">← Back</button>
            <h1>Apply Now</h1>
            <p class="subhead">Complete your professional profile below.</p>

            <form id="applicationForm" onsubmit="event.preventDefault(); submitApp();">
                <div class="section-title">1. Identity</div>
                <div class="form-group">
                    <label>Full name</label>
                    <input type="text" id="fullName" placeholder="e.g. Alex Rivera" autocomplete="off">
                </div>
                <div style="display: flex; gap: 1rem;">
                    <div class="form-group" style="flex:1;">
                        <label>Phone</label>
                        <input type="tel" id="phone" placeholder="(415) 555‑1234">
                    </div>
                    <div class="form-group" style="flex:1;">
                        <label>Email</label>
                        <input type="email" id="email" placeholder="a.rivera@example.com">
                    </div>
                </div>

                <div class="section-title">2. Expertise</div>
                <div class="form-group">
                    <label>Skills (multi‑select simulation)</label>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; background: rgba(0,0,0,0.2); padding: 0.8rem; border-radius: 14px; border:1px solid rgba(255,255,255,0.05);">
                        <span class="chip" data-skill="sat">Satellite</span>
                        <span class="chip" data-skill="starlink">Starlink</span>
                        <span class="chip" data-skill="tv">TV Mounting</span>
                        <span class="chip" data-skill="lowv">Low Voltage</span>
                    </div>
                    <input type="hidden" id="skillsInput" value="[]">
                </div>

                <div class="form-group">
                    <label>Experience</label>
                    <select id="experience">
                        <option value="" disabled selected>– select –</option>
                        <option value="<1 year">< 1 year</option>
                        <option value="1-2 years">1‑2 years</option>
                        <option value="3-5 years">3‑5 years</option>
                        <option value="5+ years">5+ years</option>
                    </select>
                </div>

                <div class="section-title">3. Logistics</div>
                <div style="margin-bottom: 1.5rem;">
                    <label style="margin-bottom: 0.6rem;">Truck / Van?</label>
                    <div class="radio-group">
                        <label class="radio-option"><input type="radio" name="vehicle" value="Yes"> Yes</label>
                        <label class="radio-option"><input type="radio" name="vehicle" value="No"> No</label>
                    </div>
                </div>
                <div style="margin-bottom: 2rem;">
                    <label style="margin-bottom: 0.6rem;">28ft ladder?</label>
                    <div class="radio-group">
                        <label class="radio-option"><input type="radio" name="ladder" value="Yes"> Yes</label>
                        <label class="radio-option"><input type="radio" name="ladder" value="No"> No</label>
                    </div>
                </div>

                <button type="submit" class="btn-primary" id="submitAppBtn">Submit Application →</button>
            </form>
        </div>

        <!-- page 3: success (hidden) -->
        <div id="successPage" class="page text-center" style="display: none; padding: 2rem 1rem;">
            <div class="success-icon">✅</div>
            <h1 style="font-size: 2.8rem;">Success</h1>
            <p class="subhead" style="margin-bottom: 2rem;">Application received. We will contact you shortly.</p>
            <button class="btn-primary" id="homeBtn">← Home</button>
        </div>
    </div>

    <script>
        // simple client-side state and DB simulation (inspired by streamlit session + sqlite)
        (function() {
            // ------ UI references ------
            const landing = document.getElementById('landingPage');
            const application = document.getElementById('applicationPage');
            const success = document.getElementById('successPage');

            // navigation functions
            function showLanding() {
                landing.style.display = 'block';
                application.style.display = 'none';
                success.style.display = 'none';
            }
            function showApplication() {
                landing.style.display = 'none';
                application.style.display = 'block';
                success.style.display = 'none';
                // optional: clear old form? we keep values for demo.
            }
            function showSuccess() {
                landing.style.display = 'none';
                application.style.display = 'none';
                success.style.display = 'block';
            }

            // event listeners
            document.getElementById('beginBtn').addEventListener('click', (e) => {
                e.preventDefault();
                showApplication();
            });

            document.getElementById('backToLandingBtn').addEventListener('click', (e) => {
                e.preventDefault();
                showLanding();
            });

            document.getElementById('homeBtn').addEventListener('click', (e) => {
                e.preventDefault();
                showLanding();
            });

            // ------ skills multiselect simulation (chip toggles) ------
            const skillChips = document.querySelectorAll('.chip');
            const skillsHidden = document.getElementById('skillsInput');
            let selectedSkills = [];

            skillChips.forEach(chip => {
                chip.addEventListener('click', () => {
                    const skill = chip.innerText.trim(); // Satellite, Starlink, etc.
                    const idx = selectedSkills.indexOf(skill);
                    if (idx === -1) {
                        selectedSkills.push(skill);
                        chip.style.background = 'rgba(59,130,246,0.3)';
                        chip.style.borderColor = '#3B82F6';
                    } else {
                        selectedSkills.splice(idx, 1);
                        chip.style.background = 'rgba(255,255,255,0.04)';
                        chip.style.borderColor = 'rgba(255,255,255,0.1)';
                    }
                    skillsHidden.value = JSON.stringify(selectedSkills);
                });
            });

            // ------ form submit: save to localStorage (simulate DB) & show success ------
            window.submitApp = function() {
                const name = document.getElementById('fullName').value.trim();
                const phone = document.getElementById('phone').value.trim();
                const email = document.getElementById('email').value.trim();
                const skills = selectedSkills;  // from hidden or array
                const years = document.getElementById('experience').value;
                const vehicle = document.querySelector('input[name="vehicle"]:checked')?.value || '';
                const ladder = document.querySelector('input[name="ladder"]:checked')?.value || '';

                if (!name || !phone) {
                    alert('Fields required: name and phone.');
                    return;
                }

                // build applicant object (mirror original)
                const applicant = {
                    name: name,
                    phone: phone,
                    email: email || '',
                    city: '', state: '', zip: '',          // placeholders
                    skills: skills,
                    years_exp: years || 'not specified',
                    roof_work: '',
                    vehicle: vehicle,
                    ladder: ladder,
                    license: '',
                    tools: '[]',
                    insurance: '',
                    service_area: '',
                    start_date: 'Immediate',
                    status: 'PENDING',
                    timestamp: new Date().toISOString()
                };

                // save to localStorage (simulate SQLite) – array of applicants
                let applicants = JSON.parse(localStorage.getItem('vergecom_applicants') || '[]');
                applicants.push(applicant);
                localStorage.setItem('vergecom_applicants', JSON.stringify(applicants));

                // show success page
                showSuccess();

                // (optional) reset form fields
                document.getElementById('fullName').value = '';
                document.getElementById('phone').value = '';
                document.getElementById('email').value = '';
                selectedSkills = [];
                skillsHidden.value = '[]';
                skillChips.forEach(chip => {
                    chip.style.background = 'rgba(255,255,255,0.04)';
                    chip.style.borderColor = 'rgba(255,255,255,0.1)';
                });
                document.getElementById('experience').value = '';
                const radioVehicles = document.querySelectorAll('input[name="vehicle"]');
                radioVehicles.forEach(r => r.checked = false);
                const radioLadders = document.querySelectorAll('input[name="ladder"]');
                radioLadders.forEach(r => r.checked = false);
            };

            // for demo, show landing initially.
            showLanding();

            // optional: log stored apps to console (like DB)
            console.log('stored applicants:', JSON.parse(localStorage.getItem('vergecom_applicants') || '[]'));
        })();
    </script>
    <!-- note: original streamlit code used sqlite & session state, we simulate with localStorage -->
    <!-- developer hint: no back‑end, but fully functional front‑end prototype -->
</body>
</html>
